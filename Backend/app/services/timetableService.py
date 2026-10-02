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


def generate_timetable(school_id, term_id, grade_id, regenerate=False):
    if regenerate:
        delete_entries_for_term(term_id)

    solver_input = build_solver_input(school_id, term_id, grade_id)
    units_by_id = {u.unit_id: u for u in solver_input.units}

    placements = solve(solver_input)
    if placements is None:
        raise ValueError(
            "No valid timetable could be generated for this grade — check that lesson "
            "counts, teacher availability, and resource capacity are consistent."
        )

    entries = build_timetable_entries(term_id, units_by_id, placements)
    bulk_add_entries(entries)
    return entries


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