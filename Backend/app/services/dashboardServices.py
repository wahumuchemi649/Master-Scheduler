# app/services/dashboard_service.py
from app.models.data import Grade, Stream
from app.repositories.teacher import get_all_teachers
from app.repositories.subjects import get_all_subjects
from app.repositories.periods import get_all_periods


def get_school_summary(school_id):
    grades = Grade.query.filter_by(schoolId=school_id).all()
    grade_ids = [g.id for g in grades]
    stream_count = Stream.query.filter(Stream.gradeId.in_(grade_ids)).count() if grade_ids else 0

    return {
        "gradeCount": len(grades),
        "streamCount": stream_count,
        "teacherCount": len(get_all_teachers(school_id)),
        "subjectCount": len(get_all_subjects(school_id)),
        "periodCount": len(get_all_periods(school_id)),
    }