# app/routes/teacher_assignments.py
from flask import Blueprint, request, jsonify
from app.services.teacherAssignmentService import (
    create_assignment, list_assignments_for_teacher, remove_assignment,
)

assignments_bp = Blueprint(
    "assignments", __name__, url_prefix="/api/teachers/<int:teacher_id>/assignments"
)


@assignments_bp.route("", methods=["GET"])
def get_assignments(teacher_id):
    assignments = list_assignments_for_teacher(teacher_id)
    return jsonify([
        {
            "id": a.id, "subjectId": a.subjectId,
            "streamId": a.streamId, "optionGroupId": a.optionGroupId,
        } for a in assignments
    ]), 200


@assignments_bp.route("", methods=["POST"])
def create_assignment_route(teacher_id):
    data = request.get_json()
    try:
        assignment = create_assignment(
            teacher_id, data.get("subjectId"), data.get("streamId"), data.get("optionGroupId"),
        )
        return jsonify({"id": assignment.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@assignments_bp.route("/<int:assignment_id>", methods=["DELETE"])
def delete_assignment_route(teacher_id, assignment_id):
    try:
        remove_assignment(assignment_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404