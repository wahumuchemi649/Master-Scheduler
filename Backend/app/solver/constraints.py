def teacher_available(state, teacher_id, day, period_id):
    if state.teacher_busy.get((day, period_id, teacher_id)):
        return False
    for c in state.input.teacher_constraints:
        if c.teacher_id != teacher_id or c.type != "unavailable":
            continue
        if c.parameters.get("day") != day:
            continue
        blocked_period_ids = c.parameters.get("period_ids")
        if blocked_period_ids is None:
            return False  # no period_ids specified — whole day is blocked
        if period_id in blocked_period_ids:
            return False
    return True


def owner_available(state, owner_type, owner_id, day, period_id):
    return not state.owner_busy.get((day, period_id, owner_type, owner_id))


def resource_available(state, resource_id, day, period_id):
    if resource_id is None:
        return True
    capacity = state.input.resource_capacity.get(resource_id, 1)
    booked = state.resource_bookings.get((day, period_id, resource_id), 0)
    return booked < capacity


def under_daily_subject_max(state, owner_type, owner_id, subject_id, day, max_per_day, lessons_to_add):
    if max_per_day is None:
        return True
    current = state.subject_day_count.get((owner_type, owner_id, subject_id, day), 0)
    return (current + lessons_to_add) <= max_per_day


def within_max_consecutive(state, teacher_id, day, candidate_period_indices):
    limit = None
    for c in state.input.teacher_constraints:
        if c.teacher_id == teacher_id and c.type == "max_consecutive_lessons":
            limit = c.parameters.get("max")
    if limit is None:
        return True

    occupied = set(state.teacher_day_periods.get((teacher_id, day), []))
    occupied.update(candidate_period_indices)
    ordered = sorted(occupied)

    run = 1
    longest = 1
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1] + 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    return longest <= limit