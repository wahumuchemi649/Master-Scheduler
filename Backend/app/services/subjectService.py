from app.repositories.subjects import get_subject_by_id, delete_subject
from app.repositories.subjectRequirement import delete_requirements_for_subject
from app.repositories.teacherAssignment import delete_assignments_for_subject
from app.repositories.optionBlock import delete_option_groups_for_subject
from app.repositories.timetable import delete_entries_for_subject
from app.repositories.subjects import (
    get_subject_by_id,
    get_all_subjects,
    add_subject,
    update_subject,
    delete_subject,
)
from app.repositories.school import get_school_by_id
from app.repositories.resources import get_resource_by_id


def _validate_resource(school_id, requires_resource_id):
    if requires_resource_id is None:
        return
    resource = get_resource_by_id(requires_resource_id)
    if not resource:
        raise ValueError("Resource not found")
    if resource.schoolId != school_id:
        raise ValueError("Resource does not belong to this school")


def create_subject(school_id, name, requires_resource_id=None):
    school = get_school_by_id(school_id)
    if not school:
        raise ValueError("School does not exist")
    if not name or not name.strip():
        raise ValueError("Subject name is required")

    _validate_resource(school_id, requires_resource_id)

    return add_subject(school_id, name.strip(), requires_resource_id)


def list_subjects(school_id):
    return get_all_subjects(school_id)


def edit_subject(subject_id, **fields):
    subject = get_subject_by_id(subject_id)
    if not subject:
        raise ValueError("Subject not found")

    if "requiresResourceId" in fields:
        _validate_resource(subject.schoolId, fields["requiresResourceId"])

    return update_subject(subject_id, **fields)


def remove_subject(subject_id):
    if not get_subject_by_id(subject_id):
        raise ValueError("Subject not found")

    delete_entries_for_subject(subject_id)       # placed lessons for this subject
    delete_assignments_for_subject(subject_id)   # teacher assignments to this subject
    delete_option_groups_for_subject(subject_id) # elective groups built around this subject
    delete_requirements_for_subject(subject_id)  # lesson-count requirements for this subject

    delete_subject(subject_id)
    return True