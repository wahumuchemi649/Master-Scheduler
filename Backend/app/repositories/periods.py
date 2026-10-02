from app.extensions import db
from app.models.data import Period

def get_period_by_id(period_id):
    return Period.query.get(period_id)


def get_all_periods(school_id):
    return Period.query.filter_by(schoolId=school_id).order_by(Period.startTime).all()


def add_period(school_id, start_time, end_time, label, is_teaching_period):
    new_period = Period(
        schoolId=school_id,
        startTime=start_time,
        endTime=end_time,
        label=label,
        isTeachingPeriod=is_teaching_period,
    )
    db.session.add(new_period)
    db.session.commit()
    return new_period


def update_period(period_id, **fields):
    period = Period.query.get(period_id)
    if not period:
        return None
    for key, value in fields.items():
        setattr(period, key, value)
    db.session.commit()
    return period


def delete_period(period_id):
    period = Period.query.get(period_id)
    if not period:
        return False
    db.session.delete(period)
    db.session.commit()
    return True