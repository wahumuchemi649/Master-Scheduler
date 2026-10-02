# app/routes/optionGroupAssignmentsRoute.py
from flask import Blueprint, jsonify
from app.repositories.teacherAssignment import get_assignments_for_option_group
from app.repositories.teacher import get_teacher_by_id

option_group_assignments_bp = Blueprint(
    "option_group_assignments", __name__, url_prefix="/api/option-groups/<int:option_group_id>/assignments"
)


@option_group_assignments_bp.route("", methods=["GET"])
def list_assignments(option_group_id):
    assignments = get_assignments_for_option_group(option_group_id)
    result = [
        {"assignmentId": a.id, "teacherId": a.teacherId, "teacherName": (get_teacher_by_id(a.teacherId) or {}).name if get_teacher_by_id(a.teacherId) else "—"}
        for a in assignments
    ]
    return jsonify(result), 200