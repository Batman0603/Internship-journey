from flask import Blueprint, jsonify, request
from auth.rbac import role_required
from user_service.service import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required(["admin"])
def get_user(user_id):
    user = UserService.get_user_by_email(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role})
