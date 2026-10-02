# app/repositories/teacher_repository.py
from app.extensions import db
from app.models.data import Teacher


def get_teacher_by_id(teacher_id):
    return Teacher.query.get(teacher_id)


def get_all_teachers(school_id):
    return Teacher.query.filter_by(schoolId=school_id).all()


def add_teacher(school_id, name, phonenumber):
    new_teacher = Teacher(schoolId=school_id, name=name, phonenumber=phonenumber)
    db.session.add(new_teacher)
    db.session.commit()
    return new_teacher


def update_teacher(teacher_id, **fields):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return None
    for key, value in fields.items():
        setattr(teacher, key, value)
    db.session.commit()
    return teacher


def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return False
    db.session.delete(teacher)
    db.session.commit()
    return True