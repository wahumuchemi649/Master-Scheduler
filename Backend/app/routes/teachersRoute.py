# app/routes/teachers.py
from flask import Blueprint, request, jsonify
from app.services.teacherOverviewService import get_teachers_overview
from app.services.teacherService import (
    register_teacher, list_teachers, update_teacher_details, remove_teacher,
)

teachers_bp = Blueprint("teachers", __name__, url_prefix="/api/schools/<string:school_id>/teachers")


@teachers_bp.route("", methods=["GET"])
def get_teachers(school_id):
    teachers = list_teachers(school_id)
    return jsonify([
        {"id": t.id, "name": t.name, "phonenumber": t.phonenumber} for t in teachers
    ]), 200


@teachers_bp.route("", methods=["POST"])
def create_teacher(school_id):
    data = request.get_json()
    try:
        teacher = register_teacher(school_id, data.get("name"), data.get("phonenumber"))
        return jsonify({"id": teacher.id, "name": teacher.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@teachers_bp.route("/<int:teacher_id>", methods=["PATCH"])
def patch_teacher(school_id, teacher_id):
    data = request.get_json()
    try:
        teacher = update_teacher_details(teacher_id, **data)
        return jsonify({"id": teacher.id, "name": teacher.name}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher_route(school_id, teacher_id):
    try:
        remove_teacher(teacher_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@teachers_bp.route("/overview", methods=["GET"])
def get_teachers_overview_route(school_id):
    return jsonify(get_teachers_overview(school_id)), 200    