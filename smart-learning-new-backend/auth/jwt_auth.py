from flask import request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import os
from user_service.service import UserService
import bcrypt
from utils.database import get_db
from sqlalchemy.orm import Session

def _create_token_and_response(user, message):
    """Helper to create token and response for login/signup."""
    # Create the claims for the JWT
    additional_claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    response_data = {"message": message, "role": user.role, "access_token": access_token}
    response = jsonify(response_data)

    set_access_cookies(response, access_token)
    return response

def handle_login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        db: Session = next(get_db())
        user = UserService.get_user_by_email(db, email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return jsonify({"error": "Incorrect password"}), 401

        return _create_token_and_response(user, "Login successful")

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

def handle_signup():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "student")

        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        db: Session = next(get_db())
        user = UserService.create_user(db, username, email, password, role)
        if user:
            return _create_token_and_response(user, "User created successfully")

        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500

def handle_logout():
    """Logs the user out by clearing the access_token cookie."""
    try:
        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        return jsonify({"error": f"Logout failed: {str(e)}"}), 500
