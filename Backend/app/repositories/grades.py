# app/repositories/grade_repository.py
from app.extensions import db
from app.models.data import Grade, Stream


def get_all_grades(school_id):
    return Grade.query.filter_by(schoolId=school_id).all()


def get_grade_by_id(grade_id):
    return Grade.query.get(grade_id)


def count_forms(school_id):
    return Grade.query.filter_by(schoolId=school_id).count()


def add_form(school_id, grade_name):
    new_grade = Grade(schoolId=school_id, grade_name=grade_name)
    db.session.add(new_grade)
    db.session.commit()
    return new_grade


def delete_grade(grade_id):
    grade = Grade.query.get(grade_id)
    if not grade:
        return False
    db.session.delete(grade)
    db.session.commit()
    return True


def get_streams_for_grade(grade_id):
    return Stream.query.filter_by(gradeId=grade_id).all()


def count_streams_for_grade(grade_id):
   
    return Stream.query.filter_by(gradeId=grade_id).count()


def add_stream(grade_id, stream_name):
    new_stream = Stream(gradeId=grade_id, streamName=stream_name)
    db.session.add(new_stream)
    db.session.commit()
    return new_stream


def delete_stream(stream_id):
    stream = Stream.query.get(stream_id)
    if not stream:
        return False
    db.session.delete(stream)
    db.session.commit()
    return True