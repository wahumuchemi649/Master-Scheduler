from app.repositories.teacherConstraint import (
    get_constraint_by_id, get_constraints_for_teacher, add_constraint, delete_constraint,
)

VALID_TYPES = {"unavailable", "max_consecutive_lessons"}
VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}


def create_constraint(teacher_id, constraint_type, parameters):
    if constraint_type not in VALID_TYPES:
        raise ValueError(f"constraint_type must be one of {VALID_TYPES}")

    if constraint_type == "unavailable":
        if parameters.get("day") not in VALID_DAYS:
            raise ValueError("'unavailable' constraints require a valid 'day'")
        if "period_ids" in parameters and not isinstance(parameters["period_ids"], list):
            raise ValueError("'period_ids' must be a list of period ids")

    if constraint_type == "max_consecutive_lessons":
        if "max" not in parameters or not isinstance(parameters["max"], int) or parameters["max"] < 1:
            raise ValueError("'max_consecutive_lessons' requires a positive integer 'max'")

    return add_constraint(teacher_id, constraint_type, parameters)


def list_constraints_for_teacher(teacher_id):
    return get_constraints_for_teacher(teacher_id)


def remove_constraint(constraint_id):
    if not delete_constraint(constraint_id):
        raise ValueError("Constraint not found")
    return True