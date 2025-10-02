from flask import Blueprint, jsonify, request, g
from auth.rbac import login_required
from user_service.service import UserService

user_bp = Blueprint("user_profile", __name__)

@user_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    # g.user is set by the @login_required decorator
    user = g.user
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200

@user_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    user_id = g.user.id
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username and not email:
        return jsonify({"error": "Username or email is required for update"}), 400

    updated_user = UserService.update_user(user_id, username, email)

    if updated_user == "IntegrityError":
        return jsonify({"error": "Username or email already exists"}), 409
    
    return jsonify({"message": "Profile updated successfully"}), 200