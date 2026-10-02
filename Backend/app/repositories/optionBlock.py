from app.extensions import db
from app.models.data import OptionBlock, OptionGroup


def get_option_block_by_id(option_block_id):
    return OptionBlock.query.get(option_block_id)


def get_option_blocks_for_grade(grade_id):
    return OptionBlock.query.filter_by(gradeId=grade_id).all()


def add_option_block(grade_id):
    new_block = OptionBlock(gradeId=grade_id)
    db.session.add(new_block)
    db.session.commit()
    return new_block


def delete_option_block(option_block_id):
    block = OptionBlock.query.get(option_block_id)
    if not block:
        return False
    db.session.delete(block)
    db.session.commit()
    return True


def get_option_groups_for_block(option_block_id):
    return OptionGroup.query.filter_by(optionBlockId=option_block_id).all()


def add_option_group(option_block_id, subject_id):
    new_group = OptionGroup(optionBlockId=option_block_id, subjectId=subject_id)
    db.session.add(new_group)
    db.session.commit()
    return new_group


def delete_option_group(option_group_id):
    group = OptionGroup.query.get(option_group_id)
    if not group:
        return False
    db.session.delete(group)
    db.session.commit()
    return True