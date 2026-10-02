# app/routes/constraintsOverviewRoute.py
from flask import Blueprint, request, jsonify
from app.services.constraintOverviewService import get_constraints_overview
from app.services.teacherConstraintService import create_constraint, remove_constraint

constraints_overview_bp = Blueprint(
    "constraints_overview", __name__, url_prefix="/api/schools/<string:school_id>/constraints"
)


@constraints_overview_bp.route("", methods=["GET"])
def get_overview(school_id):
    return jsonify(get_constraints_overview(school_id)), 200


@constraints_overview_bp.route("", methods=["POST"])
def create_overview(school_id):
    data = request.get_json()
    try:
        c = create_constraint(data.get("teacherId"), data.get("type"), data.get("parameters", {}))
        return jsonify({"id": c.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@constraints_overview_bp.route("/<int:constraint_id>", methods=["DELETE"])
def delete_overview(school_id, constraint_id):
    try:
        remove_constraint(constraint_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404