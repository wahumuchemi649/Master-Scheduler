# app/routes/gradesRoute.py
from flask import Blueprint, request, jsonify
from app.services.gradeService import (
    create_grade, list_grades, remove_grade,
    create_stream, list_streams, remove_stream,
)

grades_bp = Blueprint("grades", __name__, url_prefix="/api/schools/<string:school_id>/grades")


@grades_bp.route("", methods=["GET"])
def get_grades(school_id):
    grades = list_grades(school_id)
    return jsonify([{"id": g.id, "grade_name": g.grade_name} for g in grades]), 200


@grades_bp.route("", methods=["POST"])
def create_grade_route(school_id):
    data = request.get_json()
    try:
        grade = create_grade(school_id, data.get("grade_name"))
        return jsonify({"id": grade.id, "grade_name": grade.grade_name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@grades_bp.route("/<int:grade_id>", methods=["DELETE"])
def delete_grade_route(school_id, grade_id):
    try:
        remove_grade(grade_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@grades_bp.route("/<int:grade_id>/streams", methods=["GET"])
def get_streams(school_id, grade_id):
    streams = list_streams(grade_id)
    return jsonify([{"id": s.id, "streamName": s.streamName} for s in streams]), 200


@grades_bp.route("/<int:grade_id>/streams", methods=["POST"])
def create_stream_route(school_id, grade_id):
    data = request.get_json()
    try:
        stream = create_stream(grade_id, data.get("stream_name"))
        return jsonify({"id": stream.id, "streamName": stream.streamName}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@grades_bp.route("/<int:grade_id>/streams/<int:stream_id>", methods=["DELETE"])
def delete_stream_route(school_id, grade_id, stream_id):
    try:
        remove_stream(stream_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404