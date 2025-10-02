from flask import Blueprint, jsonify, request
from auth.rbac import role_required
from user_service.service import UserService
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required(["admin"])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role})

@admin_bp.route("/users", methods=["GET"])
@role_required(["admin"])
def get_all_users():
    users = UserService.get_all_users()
    users_list = [
        {"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users
    ]
    return jsonify(users_list), 200

@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@role_required(["admin"])
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get("role")
    if not new_role or new_role not in ['student', 'teacher', 'admin']:
        return jsonify({"error": "Valid role is required"}), 400
    user = UserService.update_user_role(user_id, new_role)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User role updated successfully", "user": {"id": user.id, "role": user.role}}), 200
