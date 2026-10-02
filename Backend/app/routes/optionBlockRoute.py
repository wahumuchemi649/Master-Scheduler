# app/routes/option_blocks.py
from flask import Blueprint, request, jsonify
from app.services.optionBlockService import (
    create_option_block, list_option_blocks, remove_option_block,
    add_group_to_block, list_groups_for_block, remove_option_group,
)

option_blocks_bp = Blueprint(
    "option_blocks", __name__, url_prefix="/api/grades/<int:grade_id>/option-blocks"
)


@option_blocks_bp.route("", methods=["GET"])
def get_option_blocks(grade_id):
    blocks = list_option_blocks(grade_id)
    return jsonify([{"id": b.id} for b in blocks]), 200


@option_blocks_bp.route("", methods=["POST"])
def create_option_block_route(grade_id):
    block = create_option_block(grade_id)
    return jsonify({"id": block.id}), 201


@option_blocks_bp.route("/<int:option_block_id>", methods=["DELETE"])
def delete_option_block_route(grade_id, option_block_id):
    try:
        remove_option_block(option_block_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@option_blocks_bp.route("/<int:option_block_id>/groups", methods=["GET"])
def get_groups(grade_id, option_block_id):
    groups = list_groups_for_block(option_block_id)
    return jsonify([{"id": g.id, "subjectId": g.subjectId} for g in groups]), 200


@option_blocks_bp.route("/<int:option_block_id>/groups", methods=["POST"])
def create_group_route(grade_id, option_block_id):
    data = request.get_json()
    try:
        group = add_group_to_block(option_block_id, data.get("subjectId"))
        return jsonify({"id": group.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@option_blocks_bp.route("/groups/<int:option_group_id>", methods=["DELETE"])
def delete_group_route(grade_id, option_group_id):
    try:
        remove_option_group(option_group_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404