from app.extensions import db
from app.models.data import SubjectRequirement


def get_requirement_by_id(requirement_id):
    return SubjectRequirement.query.get(requirement_id)


def get_requirements_for_grade(school_id, grade_id):
    return SubjectRequirement.query.filter_by(schoolId=school_id, gradeId=grade_id).all()


def get_requirement_for_subject(school_id, subject_id, grade_id):
    return SubjectRequirement.query.filter_by(
        schoolId=school_id, subjectId=subject_id, gradeId=grade_id
    ).first()


def add_requirement(school_id, subject_id, grade_id, lessons_per_week, doubles_per_week, max_lessons_per_day):
    new_requirement = SubjectRequirement(
        schoolId=school_id,
        subjectId=subject_id,
        gradeId=grade_id,
        lessonsPerWeek=lessons_per_week,
        doublesPerWeek=doubles_per_week,
        maxLessonsPerDay=max_lessons_per_day,
    )
    db.session.add(new_requirement)
    db.session.commit()
    return new_requirement


def update_requirement(requirement_id, **fields):
    requirement = SubjectRequirement.query.get(requirement_id)
    if not requirement:
        return None
    for key, value in fields.items():
        setattr(requirement, key, value)
    db.session.commit()
    return requirement


def delete_requirement(requirement_id):
    requirement = SubjectRequirement.query.get(requirement_id)
    if not requirement:
        return False
    db.session.delete(requirement)
    db.session.commit()
    return True
def delete_requirements_for_subject(subject_id):
    SubjectRequirement.query.filter_by(subjectId=subject_id).delete()
    db.session.commit()