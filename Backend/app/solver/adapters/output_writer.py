def build_timetable_entries(term_id, units_by_id, placements):
    entries = []
    for p in placements:
        unit = units_by_id[p["unit_id"]]
        entry = {
            "termId": term_id,
            "day": p["day"],
            "subjectId": unit.subject_id,
            "teacherId": unit.teacher_id,
            "periodId": p["period_id"],
            "doubleGroupId": p["double_group_id"],
            "streamId": unit.owner_id if unit.owner_type == "stream" else None,
            "optionGroupId": unit.owner_id if unit.owner_type == "option_group" else None,
        }
        entries.append(entry)
    return entries