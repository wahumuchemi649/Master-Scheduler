# app/services/grade_service.py
from app.repositories.grades import (
    get_all_grades, get_grade_by_id, add_form, delete_grade,
    get_streams_for_grade, add_stream, delete_stream,
)
from app.repositories.school import get_school_by_id


def create_grade(school_id, grade_name):
    if not get_school_by_id(school_id):
        raise ValueError("School does not exist")
    if not grade_name or not grade_name.strip():
        raise ValueError("Grade name is required")
    if any(g.grade_name.lower() == grade_name.strip().lower() for g in get_all_grades(school_id)):
        raise ValueError("This grade already exists")
    return add_form(school_id, grade_name.strip())


def list_grades(school_id):
    return get_all_grades(school_id)


def remove_grade(grade_id):
    if not delete_grade(grade_id):
        raise ValueError("Grade not found")
    return True


def create_stream(grade_id, stream_name):
    if not get_grade_by_id(grade_id):
        raise ValueError("Grade not found")
    if not stream_name or not stream_name.strip():
        raise ValueError("Stream name is required")
    if any(s.streamName.lower() == stream_name.strip().lower() for s in get_streams_for_grade(grade_id)):
        raise ValueError("This stream already exists for this grade")
    return add_stream(grade_id, stream_name.strip())


def list_streams(grade_id):
    return get_streams_for_grade(grade_id)


def remove_stream(stream_id):
    if not delete_stream(stream_id):
        raise ValueError("Stream not found")
    return True