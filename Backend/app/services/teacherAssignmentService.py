
from app.repositories.teacherAssignment import (
    get_assignment_by_id,
    get_assignments_for_teacher,
    assignment_exists,
    add_assignment,
    delete_assignment,
)


def create_assignment(teacher_id, subject_id, stream_id=None, option_group_id=None):
    if stream_id is None and option_group_id is None:
        raise ValueError("Assignment needs either a stream_id or an option_group_id")
    if stream_id is not None and option_group_id is not None:
        raise ValueError("Assignment cannot have both a stream_id and an option_group_id")

    if assignment_exists(teacher_id, subject_id, stream_id, option_group_id):
        raise ValueError("This teacher is already assigned to this subject/class")

    return add_assignment(teacher_id, subject_id, stream_id, option_group_id)


def list_assignments_for_teacher(teacher_id):
    return get_assignments_for_teacher(teacher_id)


def remove_assignment(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if not assignment:
        raise ValueError("Assignment not found")
    deleted = delete_assignment(assignment_id)
    return deleted