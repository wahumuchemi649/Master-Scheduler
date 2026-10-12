from collections import defaultdict


class GenerationError(ValueError):
    """A generation failure with a readable summary plus a list of specific problems."""

    def __init__(self, message, issues=None):
        super().__init__(message)
        self.issues = issues or []


def _name(si, kind, ident):
    return si.labels.get(kind, {}).get(ident, f"{kind} #{ident}")


def describe_unit(si, unit):
    return (
        f"{_name(si, 'subject', unit.subject_id)} for "
        f"{_name(si, unit.owner_type, unit.owner_id)} "
        f"(teacher {_name(si, 'teacher', unit.teacher_id)})"
    )


def _blocked_slots(si, teacher_id, period_index):
    """How many weekly slots this teacher has marked unavailable."""
    day_index = {d: i for i, d in enumerate(si.days)}
    P = len(si.periods)
    blocked = set()
    for c in si.teacher_constraints:
        if c.teacher_id != teacher_id or c.type != "unavailable":
            continue
        d = day_index.get(c.parameters.get("day"))
        if d is None:
            continue
        ids = c.parameters.get("period_ids")
        if ids is None:
            blocked.update((d, i) for i in range(P))
        else:
            blocked.update((d, period_index[p]) for p in ids if p in period_index)
    return len(blocked)


def validate_before_solving(si, skipped):
    """Returns a list of plain-language problems. An empty list means nothing obviously wrong."""
    issues = []
    P = len(si.periods)
    num_days = len(si.days)
    total_slots = P * num_days
    period_index = {p.id: i for i, p in enumerate(si.periods)}
    units = si.units
    units_by_id = {u.unit_id: u for u in units}

    if P == 0:
        return ["No teaching periods are set up. Add your weekly periods first."]

    if not units:
        for s in skipped:
            issues.append(
                f"{s['subjectName']} ({_name(si, s['ownerType'], s['ownerId'])}, teacher "
                f"{_name(si, 'teacher', s['teacherId'])}) has no lesson requirement for that grade. "
                f"Add one on the Subjects & requirements page."
            )
        return issues or ["No teacher has been assigned to any subject yet."]

    if any(u.doubles_per_week > 0 for u in units) and not si.double_adjacent_pairs:
        issues.append(
            "Some subjects need double lessons, but no two teaching periods are back-to-back "
            "(there is a break between every pair). Check your period times."
        )

    for u in units:
        who = describe_unit(si, u)
        if u.lessons_per_week - 2 * u.doubles_per_week < 0:
            issues.append(
                f"{who}: {u.doubles_per_week} double(s) need {2 * u.doubles_per_week} "
                f"lessons, but lessons/week is {u.lessons_per_week}."
            )
        if u.max_lessons_per_day is not None:
            if u.doubles_per_week > 0 and u.max_lessons_per_day < 2:
                issues.append(f"{who}: a double lesson needs max lessons/day of at least 2.")
            if u.lessons_per_week > u.max_lessons_per_day * num_days:
                issues.append(
                    f"{who}: {u.lessons_per_week} lessons/week can't fit with max "
                    f"{u.max_lessons_per_day}/day over {num_days} days."
                )

    owner_load, teacher_load, resource_load = defaultdict(int), defaultdict(int), defaultdict(int)
    for u in units:
        owner_load[(u.owner_type, u.owner_id)] += u.lessons_per_week
        teacher_load[u.teacher_id] += u.lessons_per_week
        if u.resource_id is not None:
            resource_load[u.resource_id] += u.lessons_per_week

    for (otype, oid), load in owner_load.items():
        if load > total_slots:
            issues.append(
                f"{_name(si, otype, oid)} has {load} lessons/week but the week only "
                f"has {total_slots} teaching slots."
            )
    for tid, load in teacher_load.items():
        available = total_slots - _blocked_slots(si, tid, period_index)
        if load > available:
            issues.append(
                f"Teacher {_name(si, 'teacher', tid)} is assigned {load} lessons/week "
                f"but only has {available} available slots after their unavailability rules."
            )
    for rid, load in resource_load.items():
        capacity = si.resource_capacity.get(rid, 1)
        if load > capacity * total_slots:
            issues.append(
                f"{_name(si, 'resource', rid)} is needed for {load} lessons/week but "
                f"can serve at most {capacity * total_slots}."
            )

    for block in si.option_blocks:
        members = [units_by_id[x] for x in block.unit_ids if x in units_by_id]
        if len({(m.lessons_per_week, m.doubles_per_week) for m in members}) > 1:
            parts = ", ".join(
                f"{_name(si, 'subject', m.subject_id)} "
                f"({m.lessons_per_week} lessons, {m.doubles_per_week} doubles)"
                for m in members
            )
            issues.append(
                "An elective split has subjects with different lessons/week or doubles/week: "
                f"{parts}. They must match, since they run at the same time."
            )
        by_teacher = defaultdict(list)
        for m in members:
            by_teacher[m.teacher_id].append(_name(si, "subject", m.subject_id))
        for tid, names in by_teacher.items():
            if len(names) > 1:
                issues.append(
                    f"Teacher {_name(si, 'teacher', tid)} is assigned to {' and '.join(names)} "
                    f"in the same elective split, so they'd have to teach both at once."
                )
    return issues


def describe_tightest(si, top=3):
    """Used when the solver finds no solution: shows which teachers and classes are closest to full."""
    total_slots = len(si.periods) * len(si.days)
    period_index = {p.id: i for i, p in enumerate(si.periods)}
    teacher_load, owner_load = defaultdict(int), defaultdict(int)
    for u in si.units:
        teacher_load[u.teacher_id] += u.lessons_per_week
        owner_load[(u.owner_type, u.owner_id)] += u.lessons_per_week

    teachers = []
    for tid, load in teacher_load.items():
        available = total_slots - _blocked_slots(si, tid, period_index)
        if available > 0:
            teachers.append((
                load / available,
                f"Teacher {_name(si, 'teacher', tid)}: {load} lessons in {available} available slots "
                f"({round(100 * load / available)}% full)",
            ))
    classes = [
        (load / total_slots,
         f"{_name(si, o[0], o[1])}: {load} of {total_slots} slots used "
         f"({round(100 * load / total_slots)}% full)")
        for o, load in owner_load.items()
    ]
    teachers.sort(reverse=True)
    classes.sort(reverse=True)
    return [t for _, t in teachers[:top]] + [t for _, t in classes[:top]]
