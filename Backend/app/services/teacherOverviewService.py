from app.models.data import Stream, Grade, OptionGroup, OptionBlock, Subject
from app.repositories.teacher import get_all_teachers
from app.repositories.teacherAssignment import get_assignments_for_teacher
from app.repositories.subjectRequirement import get_requirement_for_subject


def _grade_id_for_assignment(a):
    if a.streamId:
        stream = Stream.query.get(a.streamId)
        return stream.gradeId if stream else None
    if a.optionGroupId:
        group = OptionGroup.query.get(a.optionGroupId)
        if group:
            block = OptionBlock.query.get(group.optionBlockId)
            return block.gradeId if block else None
    return None


def _class_label_for_assignment(a):
    if a.streamId:
        stream = Stream.query.get(a.streamId)
        if stream:
            grade = Grade.query.get(stream.gradeId)
            grade_name = grade.grade_name if grade else ""
            return f"{grade_name} {stream.streamName}".strip()
    if a.optionGroupId:
        group = OptionGroup.query.get(a.optionGroupId)
        if group:
            subject = Subject.query.get(group.subjectId)
            return f"Elective: {subject.name}" if subject else "Elective"
    return "—"


def get_teachers_overview(school_id):
    teachers = get_all_teachers(school_id)
    overview = []

    for teacher in teachers:
        assignments = get_assignments_for_teacher(teacher.id)
        subject_names = set()
        class_labels = set()
        weekly_load = 0

        for a in assignments:
            subject = Subject.query.get(a.subjectId)
            if subject:
                subject_names.add(subject.name)

            class_labels.add(_class_label_for_assignment(a))

            grade_id = _grade_id_for_assignment(a)
            if grade_id:
                requirement = get_requirement_for_subject(school_id, a.subjectId, grade_id)
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