from collections import defaultdict
from app.models.data import SubjectRequirement, Subject, Grade, TeacherAssignment, Teacher, Stream


def get_requirements_overview(school_id):
    requirements = SubjectRequirement.query.filter_by(schoolId=school_id).all()
    if not requirements:
        return []

    subjects = {s.id: s for s in Subject.query.filter_by(schoolId=school_id).all()}
    grades = {g.id: g for g in Grade.query.filter_by(schoolId=school_id).all()}
    streams = {s.id: s for s in Stream.query.filter(Stream.gradeId.in_(list(grades))).all()} if grades else {}
    assignments = (
        TeacherAssignment.query.filter(TeacherAssignment.streamId.in_(list(streams))).all()
        if streams else []
    )
    teachers = {t.id: t for t in Teacher.query.filter_by(schoolId=school_id).all()}

    assignments_by_subject = defaultdict(list)
    for a in assignments:
        assignments_by_subject[a.subjectId].append(a)

    overview = []
    for r in requirements:
        subject = subjects.get(r.subjectId)
        grade = grades.get(r.gradeId)

        teacher_entries = []
        for a in assignments_by_subject[r.subjectId]:
            stream = streams.get(a.streamId)
            teacher = teachers.get(a.teacherId)
            if stream and teacher and stream.gradeId == r.gradeId:
                teacher_entries.append({
                    "assignmentId": a.id,
                    "teacherId": teacher.id,
                    "teacherName": teacher.name,
                    "streamId": stream.id,
                    "streamName": stream.streamName,
                })

        overview.append({
            "id": r.id,
            "subjectId": r.subjectId,
            "subjectName": subject.name if subject else "—",
            "gradeId": r.gradeId,
            "gradeName": grade.grade_name if grade else "—",
            "lessonsPerWeek": r.lessonsPerWeek,
            "doublesPerWeek": r.doublesPerWeek,
            "maxLessonsPerDay": r.maxLessonsPerDay,
            "teachers": teacher_entries,
        })

    return overview