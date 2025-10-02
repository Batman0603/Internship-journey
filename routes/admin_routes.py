from flask import Blueprint, jsonify, request
from auth.rbac import role_required
from user_service.service import UserService
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required(["admin"])
def get_user(admin_user, user_id): # Renamed 'user' to 'admin_user'
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role})

@admin_bp.route("/users", methods=["GET"])
@role_required(["admin"])
def get_all_users(admin_user): # Renamed 'user' to 'admin_user'
    users = UserService.get_all_users()
    users_list = [
        {"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users
    ]
    return jsonify(users_list), 200

@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@role_required(["admin"])
def update_user_role(admin_user, user_id): # Renamed 'user' to 'admin_user'
    data = request.get_json()
    new_role = data.get("role")
    if not new_role or new_role not in ['student', 'teacher', 'admin']:
        return jsonify({"error": "Valid role is required"}), 400
    updated_user = UserService.update_user_role(user_id, new_role)
    if not updated_user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User role updated successfully", "user": {"id": updated_user.id, "role": updated_user.role}}), 200