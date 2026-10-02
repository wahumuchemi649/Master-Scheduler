
from app.repositories.subjectRequirement import (
    get_requirement_by_id,
    get_requirements_for_grade,
    get_requirement_for_subject,
    add_requirement,
    update_requirement,
    delete_requirement,
)


def create_requirement(school_id, subject_id, grade_id, lessons_per_week, doubles_per_week, max_lessons_per_day):
    if lessons_per_week is None or lessons_per_week < 1:
        raise ValueError("lessons_per_week must be at least 1")

    doubles_per_week = doubles_per_week or 0
    if doubles_per_week < 0:
        raise ValueError("doubles_per_week cannot be negative")
    if doubles_per_week > lessons_per_week:
        raise ValueError("doubles_per_week cannot exceed lessons_per_week")
    # each double consumes 2 lessons, so doubles alone can't exceed half the weekly count
    if doubles_per_week * 2 > lessons_per_week:
        raise ValueError("doubles_per_week is too high for the given lessons_per_week")

    if max_lessons_per_day is not None and max_lessons_per_day < 1:
        raise ValueError("max_lessons_per_day must be at least 1")

    if get_requirement_for_subject(school_id, subject_id, grade_id):
        raise ValueError("A requirement for this subject and grade already exists")

    return add_requirement(
        school_id, subject_id, grade_id, lessons_per_week, doubles_per_week, max_lessons_per_day
    )


def list_requirements_for_grade(school_id, grade_id):
    return get_requirements_for_grade(school_id, grade_id)


def edit_requirement(requirement_id, **fields):
    requirement = get_requirement_by_id(requirement_id)
    if not requirement:
        raise ValueError("Requirement not found")
    return update_requirement(requirement_id, **fields)


def remove_requirement(requirement_id):
    deleted = delete_requirement(requirement_id)
    if not deleted:
        raise ValueError("Requirement not found")
    return True