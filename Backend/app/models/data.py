# app/models/data.py
from app.extensions import db

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    contact_name = db.Column(db.String(50))
    primary_contact = db.Column(db.String(50))
    primary_role = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))


class Term(db.Model):
    __tablename__ = "term"

    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    academic_year = db.Column(db.Integer)
    term_name = db.Column(db.String(20))


class Grade(db.Model):
    __tablename__ = "grade"

    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    grade_name = db.Column(db.String(20))


class Stream(db.Model):
    __tablename__ = "streams"

    id = db.Column(db.Integer, primary_key=True)
    gradeId = db.Column(db.Integer, db.ForeignKey("grade.id"))
    streamName = db.Column(db.String(20))

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    requiresResourceId = db.Column(db.Integer, db.ForeignKey("resources.id"))


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phonenumber = db.Column(db.Integer)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))


class TeacherAssignment(db.Model):
    __tablename__ = "teacherassignment"

    id = db.Column(db.Integer, primary_key=True)
    teacherId = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    subjectId = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    streamId = db.Column(db.Integer, db.ForeignKey("streams.id"))
    optionGroupId = db.Column(db.Integer, db.ForeignKey("optiongroup.id"))


class OptionBlock(db.Model):
    __tablename__ = "optionblock"

    id = db.Column(db.Integer, primary_key=True)
    gradeId = db.Column(db.Integer, db.ForeignKey("grade.id"))


class OptionGroup(db.Model):
    __tablename__ = "optiongroup"

    id = db.Column(db.Integer, primary_key=True)
    optionBlockId = db.Column(db.Integer, db.ForeignKey("optionblock.id"))
    subjectId = db.Column(db.Integer, db.ForeignKey("subjects.id"))


class SubjectRequirement(db.Model):
    __tablename__ = "subjectrequirement"

    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    subjectId = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    gradeId = db.Column(db.Integer, db.ForeignKey("grade.id"))
    lessonsPerWeek = db.Column(db.Integer)
    doublesPerWeek = db.Column(db.Integer)
    maxLessonsPerDay = db.Column(db.Integer)


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    name = db.Column(db.String(50))
    capacity = db.Column(db.Integer)


class Period(db.Model):
    __tablename__ = "period"

    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(20), db.ForeignKey("schools.id"))
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)
    label = db.Column(db.String(20))
    isTeachingPeriod = db.Column(db.Boolean)


class TeacherConstraint(db.Model):
    __tablename__ = "teacherconstraint"

    id = db.Column(db.Integer, primary_key=True)
    teacherId = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    type = db.Column(db.String(50))
    parameters = db.Column(db.JSON)


class TimetableEntry(db.Model):
    __tablename__ = "timetableentry"

    id = db.Column(db.Integer, primary_key=True)
    termId = db.Column(db.Integer, db.ForeignKey("term.id"))
    day = db.Column(db.String(10))
    subjectId = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    teacherId = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    periodId = db.Column(db.Integer, db.ForeignKey("period.id"))
    doubleGroupId = db.Column(db.Integer)
    streamId = db.Column(db.Integer, db.ForeignKey("streams.id"))
    optionGroupId = db.Column(db.Integer, db.ForeignKey("optiongroup.id"))