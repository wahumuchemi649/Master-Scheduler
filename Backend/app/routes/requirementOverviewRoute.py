from flask import Blueprint, request, jsonify
from app.services.requirementOverviewService import get_requirements_overview
from app.services.subjectRequirementservice import create_requirement, remove_requirement

requirements_overview_bp = Blueprint(
    "requirements_overview", __name__, url_prefix="/api/schools/<string:school_id>/requirements"
)


@requirements_overview_bp.route("", methods=["GET"])
def get_overview(school_id):
    return jsonify(get_requirements_overview(school_id)), 200


@requirements_overview_bp.route("", methods=["POST"])
def create_requirement_flat(school_id):
    data = request.get_json()
    try:
        req = create_requirement(
            school_id, data.get("subjectId"), data.get("gradeId"),
            data.get("lessonsPerWeek"), data.get("doublesPerWeek"), data.get("maxLessonsPerDay"),
        )
        return jsonify({"id": req.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@requirements_overview_bp.route("/<int:requirement_id>", methods=["DELETE"])
def delete_requirement_flat(school_id, requirement_id):
    try:
        remove_requirement(requirement_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404