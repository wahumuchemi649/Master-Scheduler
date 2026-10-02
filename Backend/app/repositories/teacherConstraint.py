from app.extensions import db
from app.models.data import TeacherConstraint


def get_constraint_by_id(constraint_id):
    return TeacherConstraint.query.get(constraint_id)


def get_constraints_for_teacher(teacher_id):
    return TeacherConstraint.query.filter_by(teacherId=teacher_id).all()


def add_constraint(teacher_id, constraint_type, parameters):
    new_constraint = TeacherConstraint(
        teacherId=teacher_id, type=constraint_type, parameters=parameters
    )
    db.session.add(new_constraint)
    db.session.commit()
    return new_constraint


def delete_constraint(constraint_id):
    constraint = TeacherConstraint.query.get(constraint_id)
    if not constraint:
        return False
    db.session.delete(constraint)
    db.session.commit()
    return True
