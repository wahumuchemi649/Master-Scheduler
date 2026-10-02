
from app.repositories.optionBlock import (
    get_option_block_by_id,
    get_option_blocks_for_grade,
    add_option_block,
    delete_option_block,
    get_option_groups_for_block,
    add_option_group,
    delete_option_group,
)


def create_option_block(grade_id):
    return add_option_block(grade_id)


def list_option_blocks(grade_id):
    return get_option_blocks_for_grade(grade_id)


def remove_option_block(option_block_id):
    deleted = delete_option_block(option_block_id)
    if not deleted:
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
    deleted = delete_option_group(option_group_id)
    if not deleted:
        raise ValueError("Option group not found")
    return True