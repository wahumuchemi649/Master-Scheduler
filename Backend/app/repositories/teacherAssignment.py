from app.extensions import db
from app.models.data import TeacherAssignment, TeacherConstraint, TimetableEntry


def get_assignment_by_id(assignment_id):
    return TeacherAssignment.query.get(assignment_id)


def get_assignments_for_teacher(teacher_id):
    return TeacherAssignment.query.filter_by(teacherId=teacher_id).all()


def get_assignments_for_stream(stream_id):
    return TeacherAssignment.query.filter_by(streamId=stream_id).all()

def get_assignments_for_option_group(option_group_id):
    return TeacherAssignment.query.filter_by(optionGroupId=option_group_id).all()

def assignment_exists(teacher_id, subject_id, stream_id=None, option_group_id=None):
    query = TeacherAssignment.query.filter_by(teacherId=teacher_id, subjectId=subject_id)
    if stream_id is not None:
        query = query.filter_by(streamId=stream_id)
    if option_group_id is not None:
        query = query.filter_by(optionGroupId=option_group_id)
    return query.first() is not None

def add_assignment(teacher_id, subject_id, stream_id=None, option_group_id=None):
    new_assignment = TeacherAssignment(
        teacherId=teacher_id,
        subjectId=subject_id,
        streamId=stream_id,
        optionGroupId=option_group_id,
    )
    db.session.add(new_assignment)
    db.session.commit()
    return new_assignment
def delete_assignment(assignment_id):
    assignment = TeacherAssignment.query.get(assignment_id)
    if not assignment:
        return False
    db.session.delete(assignment)
    db.session.commit()
    return True
def delete_assignments_for_teacher(teacher_id):
    TeacherAssignment.query.filter_by(teacherId=teacher_id).delete()
    db.session.commit()
def delete_constraints_for_teacher(teacher_id):
    TeacherConstraint.query.filter_by(teacherId=teacher_id).delete()
    db.session.commit()    
def delete_entries_for_teacher(teacher_id):
    TimetableEntry.query.filter_by(teacherId=teacher_id).delete()
    db.session.commit()    