# app/routes/resources.py
from flask import Blueprint, request, jsonify
from app.services.resourceService import (
    create_resource, list_resources, edit_resource, remove_resource,
)

resources_bp = Blueprint("resources", __name__, url_prefix="/api/schools/<string:school_id>/resources")


@resources_bp.route("", methods=["GET"])
def get_resources(school_id):
    resources = list_resources(school_id)
    return jsonify([{"id": r.id, "name": r.name, "capacity": r.capacity} for r in resources]), 200


@resources_bp.route("", methods=["POST"])
def create_resource_route(school_id):
    data = request.get_json()
    try:
        resource = create_resource(school_id, data.get("name"), data.get("capacity", 1))
        return jsonify({"id": resource.id, "name": resource.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@resources_bp.route("/<int:resource_id>", methods=["PATCH"])
def patch_resource(school_id, resource_id):
    data = request.get_json()
    try:
        resource = edit_resource(resource_id, **data)
        return jsonify({"id": resource.id, "name": resource.name}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@resources_bp.route("/<int:resource_id>", methods=["DELETE"])
def delete_resource_route(school_id, resource_id):
    try:
        remove_resource(resource_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404