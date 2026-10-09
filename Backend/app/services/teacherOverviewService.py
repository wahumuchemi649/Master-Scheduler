from app.models.data import Stream, Grade, OptionGroup, OptionBlock, Subject
from collections import defaultdict
from app.models.data import (
    Teacher, TeacherAssignment, Subject, Stream, Grade,
    OptionGroup, OptionBlock, SubjectRequirement,
)

def get_teachers_overview(school_id):
    teachers = Teacher.query.filter_by(schoolId=school_id).all()
    if not teachers:
        return []

    teacher_ids = [t.id for t in teachers]
    assignments = TeacherAssignment.query.filter(TeacherAssignment.teacherId.in_(teacher_ids)).all()

    subjects = {s.id: s for s in Subject.query.filter_by(schoolId=school_id).all()}
    grades = {g.id: g for g in Grade.query.filter_by(schoolId=school_id).all()}
    grade_ids = list(grades)
    streams = {s.id: s for s in Stream.query.filter(Stream.gradeId.in_(grade_ids)).all()} if grade_ids else {}
    blocks = {b.id: b for b in OptionBlock.query.filter(OptionBlock.gradeId.in_(grade_ids)).all()} if grade_ids else {}
    groups = (
        {g.id: g for g in OptionGroup.query.filter(OptionGroup.optionBlockId.in_(list(blocks))).all()}
        if blocks else {}
    )
    requirements = {
        (r.subjectId, r.gradeId): r
        for r in SubjectRequirement.query.filter_by(schoolId=school_id).all()
    }

    by_teacher = defaultdict(list)
    for a in assignments:
        by_teacher[a.teacherId].append(a)

    overview = []
    for teacher in teachers:
        subject_names, class_labels, weekly_load = set(), set(), 0

        for a in by_teacher[teacher.id]:
            subject = subjects.get(a.subjectId)
            if subject:
                subject_names.add(subject.name)

            grade_id = None
            if a.streamId and a.streamId in streams:
                stream = streams[a.streamId]
                grade_id = stream.gradeId
                grade = grades.get(grade_id)
                class_labels.add(f"{grade.grade_name if grade else ''} {stream.streamName}".strip())
            elif a.optionGroupId and a.optionGroupId in groups:
                group = groups[a.optionGroupId]
                block = blocks.get(group.optionBlockId)
                grade_id = block.gradeId if block else None
                group_subject = subjects.get(group.subjectId)
                class_labels.add(f"Elective: {group_subject.name}" if group_subject else "Elective")
            else:
                class_labels.add("—")

            requirement = requirements.get((a.subjectId, grade_id))
            if requirement:
                weekly_load += requirement.lessonsPerWeek or 0

        overview.append({
            "id": teacher.id,
            "name": teacher.name,
            "phonenumber": teacher.phonenumber,
            "subjects": sorted(subject_names),
            "classes": sorted(class_labels),
            "weeklyLoad": weekly_load,
        })

    return overview