# app/solver/engine.py
from ortools.sat.python import cp_model


def _group_blocks(solver_input):
    """Turn units (and option-block groups) into lists of 'blocks' — each block is
    a single lesson (size=1) or a double lesson (size=2) that needs a slot."""
    units_by_id = {u.unit_id: u for u in solver_input.units}
    blocked_unit_ids = {uid for b in solver_input.option_blocks for uid in b.unit_ids}

    tasks = []  # each: {"unit_ids": [...], "blocks": [2, 2, 1, 1, ...]}

    for block in solver_input.option_blocks:
        rep = units_by_id[block.unit_ids[0]]
        for other_id in block.unit_ids[1:]:
            other = units_by_id[other_id]
            if other.lessons_per_week != rep.lessons_per_week or other.doubles_per_week != rep.doubles_per_week:
                raise ValueError(
                    f"Option block {block.block_id}: all subjects must share the same "
                    f"lessons_per_week and doubles_per_week (mismatch between {rep.unit_id} and {other.unit_id})"
                )
        doubles = rep.doubles_per_week
        singles = rep.lessons_per_week - 2 * doubles
        tasks.append({"unit_ids": block.unit_ids, "blocks": [2] * doubles + [1] * singles})

    for unit in solver_input.units:
        if unit.unit_id in blocked_unit_ids:
            continue
        doubles = unit.doubles_per_week
        singles = unit.lessons_per_week - 2 * doubles
        tasks.append({"unit_ids": [unit.unit_id], "blocks": [2] * doubles + [1] * singles})

    return tasks


def _compute_valid_starts(size, teacher_id, solver_input, periods, period_index, adjacent_set, P, num_days, day_index):
    base = []
    if size == 2:
        for d in range(num_days):
            for i in range(P - 1):
                if (periods[i].id, periods[i + 1].id) in adjacent_set:
                    base.append((d, i))
    else:
        for d in range(num_days):
            for i in range(P):
                base.append((d, i))

    blocked = set()
    for c in solver_input.teacher_constraints:
        if c.teacher_id != teacher_id or c.type != "unavailable":
            continue
        d = day_index.get(c.parameters.get("day"))
        if d is None:
            continue
        period_ids = c.parameters.get("period_ids")
        if period_ids is None:
            blocked.add((d, "ALL"))
        else:
            for pid in period_ids:
                if pid in period_index:
                    blocked.add((d, period_index[pid]))

    valid = []
    for d, i in base:
        if (d, "ALL") in blocked:
            continue
        if size == 2 and ((d, i) in blocked or (d, i + 1) in blocked):
            continue
        if size == 1 and (d, i) in blocked:
            continue
        valid.append(d * P + i)
    return valid


def solve(solver_input, time_limit_seconds=30):
    units_by_id = {u.unit_id: u for u in solver_input.units}
    tasks = _group_blocks(solver_input)

    periods = solver_input.periods
    P = len(periods)
    days = solver_input.days
    num_days = len(days)
    day_index = {d: i for i, d in enumerate(days)}
    period_index = {p.id: i for i, p in enumerate(periods)}
    adjacent_set = set(solver_input.double_adjacent_pairs)

    model = cp_model.CpModel()
    block_vars = []  # {task, block_index, size, start, interval}

    for task in tasks:
        teacher_ids = [units_by_id[uid].teacher_id for uid in task["unit_ids"]]
        for b_idx, size in enumerate(task["blocks"]):
            # intersect valid starts across every teacher involved (matters for option-block groups)
            valid_sets = [
                set(_compute_valid_starts(size, tid, solver_input, periods, period_index, adjacent_set, P, num_days, day_index))
                for tid in teacher_ids
            ]
            domain = set.intersection(*valid_sets) if valid_sets else set()
            if not domain:
                raise ValueError(
                    f"No valid slot exists for {task['unit_ids']} (block {b_idx}) — "
                    f"check teacher availability and double-period adjacency in your period structure"
                )
            start = model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(sorted(domain)), f"start_{task['unit_ids'][0]}_{b_idx}"
            )
            interval = model.NewFixedSizeIntervalVar(start, size, f"iv_{task['unit_ids'][0]}_{b_idx}")
            block_vars.append({"task": task, "block_index": b_idx, "size": size, "start": start, "interval": interval})

    unit_blocks = {u.unit_id: [] for u in solver_input.units}
    for bv in block_vars:
        for uid in bv["task"]["unit_ids"]:
            unit_blocks[uid].append(bv)

    # teacher not double-booked
    teacher_intervals = {}
    for unit in solver_input.units:
        teacher_intervals.setdefault(unit.teacher_id, []).extend(b["interval"] for b in unit_blocks[unit.unit_id])
    for intervals in teacher_intervals.values():
        if len(intervals) > 1:
            model.AddNoOverlap(intervals)

    # owner (stream / option-group) not double-booked
    owner_intervals = {}
    for unit in solver_input.units:
        key = (unit.owner_type, unit.owner_id)
        owner_intervals.setdefault(key, []).extend(b["interval"] for b in unit_blocks[unit.unit_id])
    for intervals in owner_intervals.values():
        if len(intervals) > 1:
            model.AddNoOverlap(intervals)

    # resource capacity
    resource_intervals, resource_demands = {}, {}
    for unit in solver_input.units:
        if unit.resource_id is None:
            continue
        blocks = unit_blocks[unit.unit_id]
        resource_intervals.setdefault(unit.resource_id, []).extend(b["interval"] for b in blocks)
        resource_demands.setdefault(unit.resource_id, []).extend([1] * len(blocks))
    for rid, intervals in resource_intervals.items():
        capacity = solver_input.resource_capacity.get(rid, 1)
        model.AddCumulative(intervals, resource_demands[rid], capacity)

    # max lessons per day, per unit
    for unit in solver_input.units:
        if unit.max_lessons_per_day is None:
            continue
        blocks = unit_blocks[unit.unit_id]
        if not blocks:
            continue
        day_vars = []
        for bv in blocks:
            dv = model.NewIntVar(0, num_days - 1, f"day_{unit.unit_id}_{bv['block_index']}")
            model.AddDivisionEquality(dv, bv["start"], P)
            day_vars.append((dv, bv["size"]))
        for d in range(num_days):
            terms = []
            for dv, size in day_vars:
                is_d = model.NewBoolVar(f"isday_{unit.unit_id}_{d}_{id(dv)}")
                model.Add(dv == d).OnlyEnforceIf(is_d)
                model.Add(dv != d).OnlyEnforceIf(is_d.Not())
                terms.append(size * is_d)
            model.Add(sum(terms) <= unit.max_lessons_per_day)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status == cp_model.UNKNOWN:
        raise TimeoutError(f"Generation did not finish within {time_limit_seconds} seconds")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    double_group_counter = 0
    placements = []
    for bv in block_vars:
        start_val = solver.Value(bv["start"])
        day = days[start_val // P]
        period_id = periods[start_val % P].id
        double_group_id = None
        if bv["size"] == 2:
            double_group_counter += 1
            double_group_id = double_group_counter
        for uid in bv["task"]["unit_ids"]:
            placements.append({"unit_id": uid, "day": day, "period_id": period_id, "double_group_id": double_group_id})

    return placements