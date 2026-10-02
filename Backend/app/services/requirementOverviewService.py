from app.models.data import SubjectRequirement, Subject, Grade, TeacherAssignment, Teacher, Stream


def get_requirements_overview(school_id):
    requirements = SubjectRequirement.query.filter_by(schoolId=school_id).all()
    overview = []

    for r in requirements:
        subject = Subject.query.get(r.subjectId)
        grade = Grade.query.get(r.gradeId)

        stream_ids = [s.id for s in Stream.query.filter_by(gradeId=r.gradeId).all()]
        assignments = (
            TeacherAssignment.query.filter(
                TeacherAssignment.subjectId == r.subjectId,
                TeacherAssignment.streamId.in_(stream_ids),
            ).all()
            if stream_ids else []
        )

        teachers = []
        for a in assignments:
            teacher = Teacher.query.get(a.teacherId)
            stream = Stream.query.get(a.streamId)
            if teacher and stream:
                teachers.append({
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
            "teachers": teachers,
        })

    return overview