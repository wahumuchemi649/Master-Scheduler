# app/services/constraint_overview_service.py
from app.models.data import TeacherConstraint, Teacher


def get_constraints_overview(school_id):
    teachers = Teacher.query.filter_by(schoolId=school_id).all()
    teacher_ids = [t.id for t in teachers]
    teacher_map = {t.id: t.name for t in teachers}

    constraints = (
        TeacherConstraint.query.filter(TeacherConstraint.teacherId.in_(teacher_ids)).all()
        if teacher_ids else []
    )

    return [
        {
            "id": c.id,
            "teacherId": c.teacherId,
            "teacherName": teacher_map.get(c.teacherId, "—"),
            "type": c.type,
            "parameters": c.parameters,
        }
        for c in constraints
    ]