# app/services/timetable_service.py
from app.repositories.timetable import (
    get_entries_for_stream,
    get_entries_for_option_group,
    get_entries_for_teacher,
    get_entries_for_school,
    bulk_add_entries,
    delete_entries_for_term,
)
from app.solver.adapters.input_builder import build_solver_input
from app.solver.adapters.output_writer import build_timetable_entries
from app.solver.engine import solve


def generate_timetable(school_id, term_id, regenerate=False):
    if regenerate:
        delete_entries_for_term(term_id)

    solver_input, skipped = build_solver_input(school_id, term_id)

    if not solver_input.units:
        detail = ""
        if skipped:
            lines = [f"- {s['subjectName']} (teacher #{s['teacherId']}): {s['reason']}" for s in skipped]
            detail = " Skipped assignments:\n" + "\n".join(lines)
        raise ValueError(
            "Nothing to schedule — no teacher assignment has a matching subject requirement yet."
            + detail
        )

    units_by_id = {u.unit_id: u for u in solver_input.units}

    try:
        placements = solve(solver_input,  time_limit_seconds=30)
    except ValueError as e:
        raise ValueError(f"Could not generate: {e}")

    if placements is None:
        raise ValueError(
            "No valid timetable could be generated — the rules you've set up can't all be "
            "satisfied at once (check teacher availability, resource capacity, and lesson counts)."
        )

    entries = build_timetable_entries(term_id, units_by_id, placements)
    bulk_add_entries(entries)

    message = f"Generated {len(entries)} lessons"
    if skipped:
        message += f" ({len(skipped)} assignment(s) skipped — missing subject requirements)"

    return entries, message, skipped

def get_stream_timetable(term_id, stream_id):
    return get_entries_for_stream(term_id, stream_id)


def get_option_group_timetable(term_id, option_group_id):
    return get_entries_for_option_group(term_id, option_group_id)


def get_teacher_timetable(term_id, teacher_id):
    return get_entries_for_teacher(term_id, teacher_id)


def get_school_timetable(term_id, school_id):
    return get_entries_for_school(term_id, school_id)


def clear_term_timetable(term_id):
    return delete_entries_for_term(term_id)