# app/routes/subject_requirements.py
from flask import Blueprint, request, jsonify
from app.services.subjectRequirementservice import (
    create_requirement, list_requirements_for_grade, edit_requirement, remove_requirement,
)

requirements_bp = Blueprint(
    "requirements", __name__,
    url_prefix="/api/schools/<string:school_id>/grades/<int:grade_id>/requirements"
)


@requirements_bp.route("", methods=["GET"])
def get_requirements(school_id, grade_id):
    reqs = list_requirements_for_grade(school_id, grade_id)
    return jsonify([
        {
            "id": r.id, "subjectId": r.subjectId, "lessonsPerWeek": r.lessonsPerWeek,
            "doublesPerWeek": r.doublesPerWeek, "maxLessonsPerDay": r.maxLessonsPerDay,
        } for r in reqs
    ]), 200


@requirements_bp.route("", methods=["POST"])
def create_requirement_route(school_id, grade_id):
    data = request.get_json()
    try:
        req = create_requirement(
            school_id, data.get("subjectId"), grade_id,
            data.get("lessonsPerWeek"), data.get("doublesPerWeek"), data.get("maxLessonsPerDay"),
        )
        return jsonify({"id": req.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@requirements_bp.route("/<int:requirement_id>", methods=["PATCH"])
def patch_requirement(school_id, grade_id, requirement_id):
    data = request.get_json()
    try:
        req = edit_requirement(requirement_id, **data)
        return jsonify({"id": req.id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@requirements_bp.route("/<int:requirement_id>", methods=["DELETE"])
def delete_requirement_route(school_id, grade_id, requirement_id):
    try:
        remove_requirement(requirement_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404