# app/routes/subjects.py
from flask import Blueprint, request, jsonify
from app.services.subjectService import (
    create_subject, list_subjects, edit_subject, remove_subject,
)

subjects_bp = Blueprint("subjects", __name__, url_prefix="/api/schools/<string:school_id>/subjects")


@subjects_bp.route("", methods=["GET"])
def get_subjects(school_id):
    subjects = list_subjects(school_id)
    return jsonify([
        {"id": s.id, "name": s.name, "requiresResourceId": s.requiresResourceId} for s in subjects
    ]), 200


@subjects_bp.route("", methods=["POST"])
def create_subject_route(school_id):
    data = request.get_json()
    try:
        subject = create_subject(school_id, data.get("name"), data.get("requiresResourceId"))
        return jsonify({"id": subject.id, "name": subject.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@subjects_bp.route("/<int:subject_id>", methods=["PATCH"])
def patch_subject(school_id, subject_id):
    data = request.get_json()
    try:
        subject = edit_subject(subject_id, **data)
        return jsonify({"id": subject.id, "name": subject.name}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@subjects_bp.route("/<int:subject_id>", methods=["DELETE"])
def delete_subject_route(school_id, subject_id):
    try:
        remove_subject(subject_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404