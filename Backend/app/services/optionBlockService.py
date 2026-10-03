
from app.repositories.optionBlock import (
    get_option_block_by_id,
    get_option_blocks_for_grade,
    add_option_block,
    delete_option_block,
    get_option_groups_for_block,
    add_option_group,
    delete_option_group,
)
from app.repositories.teacherAssignment import delete_assignments_for_option_group
from app.repositories.timetable import delete_entries_for_option_group

def create_option_block(grade_id):
    return add_option_block(grade_id)


def list_option_blocks(grade_id):
    return get_option_blocks_for_grade(grade_id)


def remove_option_block(option_block_id):
    groups = get_option_groups_for_block(option_block_id)
    for g in groups:
        delete_entries_for_option_group(g.id)
        delete_assignments_for_option_group(g.id)
        delete_option_group(g.id)
    if not delete_option_block(option_block_id):
        raise ValueError("Option block not found")
    return True


def add_group_to_block(option_block_id, subject_id):
    block = get_option_block_by_id(option_block_id)
    if not block:
        raise ValueError("Option block not found")

    existing_groups = get_option_groups_for_block(option_block_id)
    if any(g.subjectId == subject_id for g in existing_groups):
        raise ValueError("This subject is already in this option block")

    return add_option_group(option_block_id, subject_id)


def list_groups_for_block(option_block_id):
    return get_option_groups_for_block(option_block_id)


def remove_option_group(option_group_id):
    delete_entries_for_option_group(option_group_id)       # placed lessons tied to this group
    delete_assignments_for_option_group(option_group_id)   # teacher assignments tied to this group
    if not delete_option_group(option_group_id):
        raise ValueError("Option group not found")
    return True