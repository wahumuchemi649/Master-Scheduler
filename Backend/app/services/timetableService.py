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
from app.solver.validation import validate_before_solving, describe_tightest, GenerationError


def generate_timetable(school_id, term_id, regenerate=False):
    if not regenerate and get_entries_for_school(term_id, school_id):
        raise GenerationError("A timetable already exists for this term.",
                              ["Tick 'Clear and regenerate' to replace it."])

    solver_input, skipped = build_solver_input(school_id, term_id)

    issues = validate_before_solving(solver_input, skipped)
    if issues:
        raise GenerationError("Generation can't start. Fix these and try again:", issues)

    units_by_id = {u.unit_id: u for u in solver_input.units}

    try:
        placements = solve(solver_input, time_limit_seconds=30)
    except ValueError as e:
        raise GenerationError("Generation stopped:", [str(e)])

    if placements is None:
        raise GenerationError(
            "No timetable satisfies every rule at once. Nothing is obviously wrong in your data, "
            "so it's a combination of rules. The fullest teachers and classes are listed below; "
            "loosen those first (fewer lessons, more availability, or another teacher).",
            describe_tightest(solver_input))

    entries = build_timetable_entries(term_id, units_by_id, placements)

    if regenerate:
        delete_entries_for_term(term_id)  # only after a new timetable exists, so a failed run can't wipe the old one
    bulk_add_entries(entries)

    message = f"Generated {len(entries)} lessons"
    if skipped:
        message += f" ({len(skipped)} assignment(s) skipped, missing subject requirements)"
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