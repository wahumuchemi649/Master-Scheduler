# app/routes/teachersConstraintsRoute.py
from flask import Blueprint, request, jsonify
from app.services.teacherConstraintService import (
    create_constraint, list_constraints_for_teacher, remove_constraint,
)

constraints_bp = Blueprint(
    "constraints", __name__, url_prefix="/api/teachers/<int:teacher_id>/constraints"
)


@constraints_bp.route("", methods=["GET"])
def get_constraints(teacher_id):
    constraints = list_constraints_for_teacher(teacher_id)
    return jsonify([
        {"id": c.id, "type": c.type, "parameters": c.parameters} for c in constraints
    ]), 200


@constraints_bp.route("", methods=["POST"])
def create_constraint_route(teacher_id):
    data = request.get_json()
    try:
        constraint = create_constraint(teacher_id, data.get("type"), data.get("parameters", {}))
        return jsonify({"id": constraint.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@constraints_bp.route("/<int:constraint_id>", methods=["DELETE"])
def delete_constraint_route(teacher_id, constraint_id):
    try:
        remove_constraint(constraint_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404