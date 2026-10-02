# app/routes/schools.py
from flask import Blueprint, request, jsonify
from app.services.schoolService import get_school_details
from app.repositories.school import get_current_term
from app.services.dashboardServices import get_school_summary
from app.services.termService import create_term

schools_bp = Blueprint("schools", __name__, url_prefix="/api/schools")


@schools_bp.route("/<string:school_id>", methods=["GET"])
def get_school(school_id):
    details = get_school_details(school_id)
    if not details:
        return jsonify({"error": "School not found"}), 404
    return jsonify(details), 200


@schools_bp.route("/<string:school_id>/current-term", methods=["GET"])
def get_school_current_term(school_id):
    term = get_current_term(school_id)
    if not term:
        return jsonify({"error": "No term found for this school"}), 404
    return jsonify({
        "id": term.id,
        "academic_year": term.academic_year,
        "term_name": term.term_name,
    }), 200    


@schools_bp.route("/<string:school_id>/summary", methods=["GET"])
def get_summary(school_id):
    return jsonify(get_school_summary(school_id)), 200
# add to app/routes/schools.py


@schools_bp.route("/<string:school_id>/term", methods=["POST"])
def create_term_route(school_id):
    data = request.get_json()
    try:
        term = create_term(school_id, data.get("academic_year"), data.get("term_name"))
        return jsonify({"id": term.id, "academic_year": term.academic_year, "term_name": term.term_name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

