# app/routes/auth.py
from flask import Blueprint, request, jsonify, session
from app.services.auth_service import signup_school, login_school


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        school = signup_school(
            data.get("name"), data.get("address"), data.get("contactName"),
            data.get("primaryContact"), data.get("primaryRole"),
            data.get("email"), data.get("password"),
        )
        session["school_id"] = school.id
        return jsonify({"id": school.id, "name": school.name, "email": school.email}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        school = login_school(data.get("email"), data.get("password"))
        session["school_id"] = school.id
        return jsonify({"id": school.id, "name": school.name, "email": school.email}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("school_id", None)
    return "", 204

@auth_bp.route("/me", methods=["GET"])
def me():
    school_id = session.get("school_id")
    if not school_id:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"id": school_id}), 200



