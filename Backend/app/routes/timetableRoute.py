# app/routes/timetable.py
from flask import Blueprint, request, jsonify
from app.services.timetableService import (
    generate_timetable, get_stream_timetable, get_option_group_timetable,
    get_teacher_timetable, get_school_timetable,
)

timetable_bp = Blueprint("timetable", __name__, url_prefix="/api/timetable")


@timetable_bp.route("/generate", methods=["POST"])
def generate_route():
    data = request.get_json()
    try:
        entries, message, skipped = generate_timetable(
            data.get("schoolId"), data.get("termId"), data.get("regenerate", False),
        )
        return jsonify({"message": message, "entries": entries, "skipped": skipped}), 201
    except TimeoutError as e:
        return jsonify({"error": str(e)}), 408
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def _serialize_entries(entries):
    return jsonify([
        {
            "id": e.id, "day": e.day, "subjectId": e.subjectId, "teacherId": e.teacherId,
            "periodId": e.periodId, "doubleGroupId": e.doubleGroupId,
            "streamId": e.streamId, "optionGroupId": e.optionGroupId,
        } for e in entries
    ]), 200


@timetable_bp.route("/term/<int:term_id>/stream/<int:stream_id>", methods=["GET"])
def stream_timetable(term_id, stream_id):
    return _serialize_entries(get_stream_timetable(term_id, stream_id))


@timetable_bp.route("/term/<int:term_id>/option-group/<int:option_group_id>", methods=["GET"])
def option_group_timetable(term_id, option_group_id):
    return _serialize_entries(get_option_group_timetable(term_id, option_group_id))


@timetable_bp.route("/term/<int:term_id>/teacher/<int:teacher_id>", methods=["GET"])
def teacher_timetable(term_id, teacher_id):
    return _serialize_entries(get_teacher_timetable(term_id, teacher_id))


@timetable_bp.route("/term/<int:term_id>/school/<string:school_id>", methods=["GET"])
def school_timetable(term_id, school_id):
    return _serialize_entries(get_school_timetable(term_id, school_id))