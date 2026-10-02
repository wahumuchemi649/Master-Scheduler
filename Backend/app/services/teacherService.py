
from app.repositories.teacher import (
    get_teacher_by_id, get_all_teachers, add_teacher, update_teacher, delete_teacher,
)
from app.repositories.teacherAssignment import delete_assignments_for_teacher, delete_constraints_for_teacher,delete_entries_for_teacher

from app.repositories.teacher import (
    get_teacher_by_id,
    get_all_teachers,
    add_teacher,
    update_teacher,
    delete_teacher,
)
from app.repositories.school import get_school_by_id


def register_teacher(school_id, name, phonenumber=None):
    school = get_school_by_id(school_id)
    if not school:
        raise ValueError("School does not exist")
    if not name or not name.strip():
        raise ValueError("Teacher name is required")
    return add_teacher(school_id, name.strip(), phonenumber)


def list_teachers(school_id):
    return get_all_teachers(school_id)


def update_teacher_details(teacher_id, **fields):
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        raise ValueError("Teacher not found")
    return update_teacher(teacher_id, **fields)




def remove_teacher(teacher_id):
    teacher = get_teacher_by_id(teacher_id)
    if not teacher:
        raise ValueError("Teacher not found")

    delete_entries_for_teacher(teacher_id)       # remove their placed lessons from any generated timetable
    delete_assignments_for_teacher(teacher_id)   # remove what they were assigned to teach
    delete_constraints_for_teacher(teacher_id)   # remove their availability rules

    delete_teacher(teacher_id)
    return True