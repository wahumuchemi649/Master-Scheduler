# app/routes/assignmentsFlatRoute.py
from flask import Blueprint, jsonify
from app.services.teacherAssignmentService import remove_assignment

assignments_flat_bp = Blueprint("assignments_flat", __name__, url_prefix="/api/assignments")


@assignments_flat_bp.route("/<int:assignment_id>", methods=["DELETE"])
def delete_assignment_flat(assignment_id):
    try:
        remove_assignment(assignment_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404