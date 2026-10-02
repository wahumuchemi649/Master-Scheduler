from app.extensions import db
from app.models.data import Subject


def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)


def get_all_subjects(school_id):
    return Subject.query.filter_by(schoolId=school_id).all()


def add_subject(school_id, name, requires_resource_id=None):
    new_subject = Subject(
        schoolId=school_id,
        name=name,
        requiresResourceId=requires_resource_id,
    )
    db.session.add(new_subject)
    db.session.commit()
    return new_subject


def update_subject(subject_id, **fields):
    subject = Subject.query.get(subject_id)
    if not subject:
        return None
    for key, value in fields.items():
        setattr(subject, key, value)
    db.session.commit()
    return subject


def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        return False
    db.session.delete(subject)
    db.session.commit()
    return True