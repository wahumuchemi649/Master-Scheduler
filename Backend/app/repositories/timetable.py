from app.extensions import db
from app.models.data import TimetableEntry


def get_entries_for_stream(term_id, stream_id):
    return TimetableEntry.query.filter_by(termId=term_id, streamId=stream_id).all()


def get_entries_for_option_group(term_id, option_group_id):
    return TimetableEntry.query.filter_by(termId=term_id, optionGroupId=option_group_id).all()


def get_entries_for_teacher(term_id, teacher_id):
    return TimetableEntry.query.filter_by(termId=term_id, teacherId=teacher_id).all()


def get_entries_for_school(term_id, school_id):
    from app.models.data import Subject

    return (
        TimetableEntry.query.join(Subject, TimetableEntry.subjectId == Subject.id)
        .filter(TimetableEntry.termId == term_id, Subject.schoolId == school_id)
        .all()
    )


def bulk_add_entries(entries):
    """entries: list of dicts matching TimetableEntry fields"""
    objects = [TimetableEntry(**entry) for entry in entries]
    db.session.bulk_save_objects(objects)
    db.session.commit()
    return objects


def delete_entries_for_term(term_id):
    TimetableEntry.query.filter_by(termId=term_id).delete()
    db.session.commit()
    return True