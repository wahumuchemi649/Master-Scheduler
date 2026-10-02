from app.solver.constraints import (
    teacher_available,
    owner_available,
    resource_available,
    under_daily_subject_max,
    within_max_consecutive,
)


class SolverState:
    def __init__(self, solver_input):
        self.input = solver_input
        self.period_index = {p.id: i for i, p in enumerate(solver_input.periods)}
        self.teacher_busy = {}
        self.owner_busy = {}
        self.resource_bookings = {}
        self.subject_day_count = {}
        self.teacher_day_periods = {}
        self.placements = []
        self._double_group_counter = 0

    def next_double_group_id(self):
        self._double_group_counter += 1
        return self._double_group_counter


def build_tasks(solver_input):
    """Flatten option blocks + standalone units into atomic placement tasks,
    ordered: block doubles, block singles, unit doubles, unit singles."""
    units_by_id = {u.unit_id: u for u in solver_input.units}
    blocked_unit_ids = {uid for b in solver_input.option_blocks for uid in b.unit_ids}

    tasks = []

    for block in solver_input.option_blocks:
        rep = units_by_id[block.unit_ids[0]]
        for other_id in block.unit_ids[1:]:
            other = units_by_id[other_id]
            if other.lessons_per_week != rep.lessons_per_week or other.doubles_per_week != rep.doubles_per_week:
                raise ValueError(
                    f"Option block {block.block_id}: all subjects in a block must share the same "
                    f"lessons_per_week and doubles_per_week (mismatch between units {rep.unit_id} and {other.unit_id})"
                )
        for _ in range(rep.doubles_per_week):
            tasks.append({"type": "block_double", "block": block})
        singles = rep.lessons_per_week - (2 * rep.doubles_per_week)
        for _ in range(singles):
            tasks.append({"type": "block_single", "block": block})

    standalone_units = [u for u in solver_input.units if u.unit_id not in blocked_unit_ids]
    for unit in standalone_units:
        for _ in range(unit.doubles_per_week):
            tasks.append({"type": "unit_double", "unit": unit})
        singles = unit.lessons_per_week - (2 * unit.doubles_per_week)
        for _ in range(singles):
            tasks.append({"type": "unit_single", "unit": unit})

    tasks.sort(key=lambda t: {"block_double": 0, "block_single": 1, "unit_double": 2, "unit_single": 3}[t["type"]])
    return tasks


def solve(solver_input):
    state = SolverState(solver_input)
    tasks = build_tasks(solver_input)
    units_by_id = {u.unit_id: u for u in solver_input.units}

    success = _backtrack(tasks, 0, state, units_by_id)
    if not success:
        return None
    return state.placements


def _backtrack(tasks, index, state, units_by_id):
    if index == len(tasks):
        return True

    task = tasks[index]
    for candidate in _generate_candidates(task, state, units_by_id):
        _apply(task, candidate, state, units_by_id)
        if _backtrack(tasks, index + 1, state, units_by_id):
            return True
        _undo(task, candidate, state, units_by_id)

    return False


def _generate_candidates(task, state, units_by_id):
    days = state.input.days

    if task["type"] in ("block_double", "unit_double"):
        for day in days:
            for (pid_a, pid_b) in state.input.double_adjacent_pairs:
                if _double_valid(task, day, pid_a, pid_b, state, units_by_id):
                    yield {"day": day, "period_ids": [pid_a, pid_b]}

    else:  # block_single, unit_single
        for day in days:
            for period in state.input.periods:
                if _single_valid(task, day, period.id, state, units_by_id):
                    yield {"day": day, "period_ids": [period.id]}


def _units_for_task(task, units_by_id):
    if task["type"].startswith("block"):
        return [units_by_id[uid] for uid in task["block"].unit_ids]
    return [task["unit"]]


def _single_valid(task, day, period_id, state, units_by_id):
    units = _units_for_task(task, units_by_id)
    idx = state.period_index[period_id]

    for unit in units:
        if not teacher_available(state, unit.teacher_id, day, period_id):
            return False
        if not owner_available(state, unit.owner_type, unit.owner_id, day, period_id):
            return False
        if not resource_available(state, unit.resource_id, day, period_id):
            return False
        if not under_daily_subject_max(
            state, unit.owner_type, unit.owner_id, unit.subject_id, day, unit.max_lessons_per_day, 1
        ):
            return False
        if not within_max_consecutive(state, unit.teacher_id, day, [idx]):
            return False

    # resource contention *between* units in the same block (different subjects, different resources, same slot)
    if not _resources_compatible_within_task(units, day, [period_id], state):
        return False

    return True


def _double_valid(task, day, pid_a, pid_b, state, units_by_id):
    units = _units_for_task(task, units_by_id)
    idx_a, idx_b = state.period_index[pid_a], state.period_index[pid_b]

    for unit in units:
        for pid, idx in ((pid_a, idx_a), (pid_b, idx_b)):
            if not teacher_available(state, unit.teacher_id, day, pid):
                return False
            if not owner_available(state, unit.owner_type, unit.owner_id, day, pid):
                return False
            if not resource_available(state, unit.resource_id, day, pid):
                return False
        if not under_daily_subject_max(
            state, unit.owner_type, unit.owner_id, unit.subject_id, day, unit.max_lessons_per_day, 2
        ):
            return False
        if not within_max_consecutive(state, unit.teacher_id, day, [idx_a, idx_b]):
            return False

    if not _resources_compatible_within_task(units, day, [pid_a, pid_b], state):
        return False

    return True


def _resources_compatible_within_task(units, day, period_ids, state):
    """Within one block placement, two different subjects might need the same resource
    at the same slot (rare, but check it) — this guards against that edge case."""
    seen = {}
    for unit in units:
        if unit.resource_id is None:
            continue
        for pid in period_ids:
            key = (day, pid, unit.resource_id)
            seen[key] = seen.get(key, 0) + 1
            capacity = state.input.resource_capacity.get(unit.resource_id, 1)
            if seen[key] > capacity:
                return False
    return True


def _apply(task, candidate, state, units_by_id):
    units = _units_for_task(task, units_by_id)
    day = candidate["day"]
    period_ids = candidate["period_ids"]
    is_double = len(period_ids) == 2
    double_group_id = state.next_double_group_id() if is_double else None

    for unit in units:
        for pid in period_ids:
            idx = state.period_index[pid]
            state.teacher_busy[(day, pid, unit.teacher_id)] = True
            state.owner_busy[(day, pid, unit.owner_type, unit.owner_id)] = True
            if unit.resource_id is not None:
                key = (day, pid, unit.resource_id)
                state.resource_bookings[key] = state.resource_bookings.get(key, 0) + 1
            state.teacher_day_periods.setdefault((unit.teacher_id, day), []).append(idx)

        day_key = (unit.owner_type, unit.owner_id, unit.subject_id, day)
        state.subject_day_count[day_key] = state.subject_day_count.get(day_key, 0) + len(period_ids)

        for pid in period_ids:
            state.placements.append({
                "unit_id": unit.unit_id, "day": day, "period_id": pid, "double_group_id": double_group_id
            })


def _undo(task, candidate, state, units_by_id):
    units = _units_for_task(task, units_by_id)
    day = candidate["day"]
    period_ids = candidate["period_ids"]

    for unit in units:
        for pid in period_ids:
            idx = state.period_index[pid]
            del state.teacher_busy[(day, pid, unit.teacher_id)]
            del state.owner_busy[(day, pid, unit.owner_type, unit.owner_id)]
            if unit.resource_id is not None:
                key = (day, pid, unit.resource_id)
                state.resource_bookings[key] -= 1
                if state.resource_bookings[key] == 0:
                    del state.resource_bookings[key]
            state.teacher_day_periods[(unit.teacher_id, day)].remove(idx)

        day_key = (unit.owner_type, unit.owner_id, unit.subject_id, day)
        state.subject_day_count[day_key] -= len(period_ids)

    for _ in range(len(units) * len(period_ids)):
        state.placements.pop()