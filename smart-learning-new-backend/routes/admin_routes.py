from flask import Blueprint, jsonify, request, Response
from auth.rbac import role_required
from user_service.service import UserService
from utils.database import get_db
from sqlalchemy.orm import Session
import os

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@role_required(["admin"])
def get_user(admin_user, user_id): # Renamed 'user' to 'admin_user'
    """
    Get a specific user by their ID.
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
    responses:
      200:
        description: User details.
      404:
        description: User not found.
    """
    db: Session = next(get_db())
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role})

@admin_bp.route("/users", methods=["GET"])
@role_required(["admin"])
def get_all_users(admin_user): # Renamed 'user' to 'admin_user'
    """
    Get a list of all users.
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: A list of all users in the system.
    """
    db: Session = next(get_db())
    users = UserService.get_all_users(db)
    users_list = [
        {"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users
    ]
    return jsonify(users_list), 200

@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@role_required(["admin"])
def update_user_role(admin_user, user_id): # Renamed 'user' to 'admin_user'
    """
    Update a user's role.
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            role:
              type: string
              enum: [student, teacher, admin]
    responses:
      200:
        description: User role updated successfully.
      400:
        description: Invalid role provided.
    """
    db: Session = next(get_db())
    data = request.get_json()
    new_role = data.get("role")
    if not new_role or new_role not in ['student', 'teacher', 'admin']:
        return jsonify({"error": "Valid role is required"}), 400
    updated_user = UserService.update_user_role(db, user_id, new_role)
    if not updated_user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User role updated successfully", "user": {"id": updated_user.id, "role": updated_user.role}}), 200

@admin_bp.route("/logs", methods=["GET"])
@role_required(["admin"])
def view_logs(admin_user):
    """
    View the application logs.
    For efficiency, it returns the last 100 lines of the log file.
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: The last 100 lines of the log file as plain text.
    """
    """
    Allows an admin to view the application logs.
    For efficiency, it returns the last 100 lines of the log file.
    """
    log_dir = os.path.abspath("logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, "flask.log")

    try:
        if not os.path.exists(log_file_path):
            return jsonify({"message": "Log file does not exist yet."}), 200

        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_100_lines = "".join(lines[-100:])
        
        return Response(last_100_lines, mimetype="text/plain")

    except Exception as e:
        return jsonify({"error": f"Could not read log file: {str(e)}"}), 500