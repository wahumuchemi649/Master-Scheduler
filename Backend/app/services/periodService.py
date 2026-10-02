# app/services/periodService.py
from datetime import datetime, time as time_type
from app.repositories.periods import (
    get_period_by_id, get_all_periods, add_period, update_period, delete_period,
)


def _parse_time(value):
    """Accepts a datetime.time (already parsed) or a string like '08:00' / '08:00:00'."""
    if isinstance(value, time_type):
        return value
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(value, fmt).time()
        except (ValueError, TypeError):
            continue
    raise ValueError(f"Invalid time format: {value!r}")


def create_period(school_id, start_time, end_time, label, is_teaching_period=True):
    start_time = _parse_time(start_time)
    end_time = _parse_time(end_time)

    if not label:
        raise ValueError("label is required")
    if start_time >= end_time:
        raise ValueError("start_time must be before end_time")

    existing = get_all_periods(school_id)
    for period in existing:
        if start_time < period.endTime and end_time > period.startTime:
            raise ValueError(f"Overlaps with existing period '{period.label}'")

    return add_period(school_id, start_time, end_time, label, is_teaching_period)


def list_periods(school_id):
    return get_all_periods(school_id)


def edit_period(period_id, **fields):
    period = get_period_by_id(period_id)
    if not period:
        raise ValueError("Period not found")
    if "startTime" in fields:
        fields["startTime"] = _parse_time(fields["startTime"])
    if "endTime" in fields:
        fields["endTime"] = _parse_time(fields["endTime"])
    return update_period(period_id, **fields)


def remove_period(period_id):
    if not delete_period(period_id):
        raise ValueError("Period not found")
    return True