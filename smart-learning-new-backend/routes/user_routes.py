from flask import Blueprint, jsonify, request, g
from auth.rbac import login_required
from user_service.service import UserService
from utils.database import get_db
from sqlalchemy.orm import Session

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

    db: Session = next(get_db())
    try:
        updated_user = UserService.update_user(db, user_id, username, email)
    except Exception as e: # Catch potential IntegrityError from the service
        if "already exists" in str(e):
            return jsonify({"error": "Username or email already exists"}), 409
        return jsonify({"error": "An unexpected error occurred"}), 500

    if updated_user:
        return jsonify({"message": "Profile updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404