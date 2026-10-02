# app/solver/adapters/input_builder.py
from app.models.data import (
    Period, Stream, OptionBlock, OptionGroup, Subject, SubjectRequirement,
    TeacherAssignment, TeacherConstraint, Resource,
)
from app.solver.structs import (
    PeriodSlot, TeachingUnit, OptionBlockGroup, TeacherConstraintData, SolverInput,
)

SCHOOL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def build_solver_input(school_id, term_id, grade_id):
    all_periods = Period.query.filter_by(schoolId=school_id).order_by(Period.startTime).all()
    teaching_periods = [p for p in all_periods if p.isTeachingPeriod]

    double_adjacent_pairs = []
    for i in range(len(all_periods) - 1):
        current, nxt = all_periods[i], all_periods[i + 1]
        if current.isTeachingPeriod and nxt.isTeachingPeriod and current.endTime == nxt.startTime:
            double_adjacent_pairs.append((current.id, nxt.id))

    period_structs = [PeriodSlot(p.id, p.label, p.startTime, p.endTime) for p in teaching_periods]

    streams = Stream.query.filter_by(gradeId=grade_id).all()
    stream_ids = {s.id for s in streams}

    option_blocks_db = OptionBlock.query.filter_by(gradeId=grade_id).all()
    option_group_ids = set()
    for block in option_blocks_db:
        groups = OptionGroup.query.filter_by(optionBlockId=block.id).all()
        option_group_ids.update(g.id for g in groups)

    requirements = SubjectRequirement.query.filter_by(schoolId=school_id, gradeId=grade_id).all()
    req_by_subject = {r.subjectId: r for r in requirements}

    # subject_id -> requiresResourceId, now sourced correctly from Subject itself
    subjects = Subject.query.filter_by(schoolId=school_id).all()
    subject_resource_map = {s.id: s.requiresResourceId for s in subjects}

    resources = Resource.query.filter_by(schoolId=school_id).all()
    resource_capacity = {r.id: r.capacity for r in resources}

    assignments = TeacherAssignment.query.filter(
        (TeacherAssignment.streamId.in_(stream_ids)) | (TeacherAssignment.optionGroupId.in_(option_group_ids))
    ).all()

    units = []
    for a in assignments:
        requirement = req_by_subject.get(a.subjectId)
        if not requirement:
            continue
        owner_type = "stream" if a.streamId else "option_group"
        owner_id = a.streamId or a.optionGroupId
        units.append(TeachingUnit(
            unit_id=f"{a.teacherId}-{a.subjectId}-{owner_type}-{owner_id}",
            teacher_id=a.teacherId,
            subject_id=a.subjectId,
            owner_type=owner_type,
            owner_id=owner_id,
            lessons_per_week=requirement.lessonsPerWeek,
            doubles_per_week=requirement.doublesPerWeek or 0,
            max_lessons_per_day=requirement.maxLessonsPerDay,
            resource_id=subject_resource_map.get(a.subjectId),
        ))

    option_block_groups = []
    for block in option_blocks_db:
        groups = OptionGroup.query.filter_by(optionBlockId=block.id).all()
        group_ids = {g.id for g in groups}
        unit_ids = [u.unit_id for u in units if u.owner_type == "option_group" and u.owner_id in group_ids]
        if unit_ids:
            option_block_groups.append(OptionBlockGroup(block_id=block.id, unit_ids=unit_ids))

    teacher_ids = {u.teacher_id for u in units}
    constraints_db = TeacherConstraint.query.filter(TeacherConstraint.teacherId.in_(teacher_ids)).all()
    teacher_constraints = [
        TeacherConstraintData(teacher_id=c.teacherId, type=c.type, parameters=c.parameters or {})
        for c in constraints_db
    ]

    return SolverInput(
        school_id=school_id,
        term_id=term_id,
        days=SCHOOL_DAYS,
        periods=period_structs,
        double_adjacent_pairs=double_adjacent_pairs,
        units=units,
        option_blocks=option_block_groups,
        teacher_constraints=teacher_constraints,
        resource_capacity=resource_capacity,
    )