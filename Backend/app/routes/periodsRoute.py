# app/routes/periods.py
from flask import Blueprint, request, jsonify
from app.services.periodService import create_period, list_periods, edit_period, remove_period

periods_bp = Blueprint("periods", __name__, url_prefix="/api/schools/<string:school_id>/periods")


@periods_bp.route("", methods=["GET"])
def get_periods(school_id):
    periods = list_periods(school_id)
    return jsonify([
        {
            "id": p.id, "label": p.label, "startTime": str(p.startTime),
            "endTime": str(p.endTime), "isTeachingPeriod": p.isTeachingPeriod,
        } for p in periods
    ]), 200


@periods_bp.route("", methods=["POST"])
def create_period_route(school_id):
    data = request.get_json()
    try:
        period = create_period(
            school_id, data.get("startTime"), data.get("endTime"),
            data.get("label"), data.get("isTeachingPeriod", True),
        )
        return jsonify({"id": period.id, "label": period.label}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@periods_bp.route("/<int:period_id>", methods=["PATCH"])
def patch_period(school_id, period_id):
    data = request.get_json()
    try:
        period = edit_period(period_id, **data)
        return jsonify({"id": period.id, "label": period.label}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@periods_bp.route("/<int:period_id>", methods=["DELETE"])
def delete_period_route(school_id, period_id):
    try:
        remove_period(period_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404