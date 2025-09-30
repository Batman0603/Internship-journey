from flask import request, jsonify
import jwt, datetime
from utils.config import Config
from user_service.service import UserService
import bcrypt

def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = UserService.get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return jsonify({"error": "Incorrect password"}), 401

        payload = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "role": user.role}), 200
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

def signup():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "student")

        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        user = UserService.create_user(username, email, password, role)
        if user:
            return jsonify({"message": "User created successfully"}), 201
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500
