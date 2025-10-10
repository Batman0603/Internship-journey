from flask import request, jsonify, make_response
import jwt, datetime
import os
from utils.config import Config
from user_service.service import UserService
import bcrypt
from utils.database import get_db
from sqlalchemy.orm import Session

def login():
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

        payload = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

        response = make_response(jsonify({"message": "Login successful", "role": user.role}), 200)
        response.set_cookie(
            'access_token',
            value=token,
            httponly=True,
            secure=os.getenv('FLASK_ENV') != 'development', # Set to True in production
            samesite='Lax',
            expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
        )
        return response

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

        db: Session = next(get_db())
        user = UserService.create_user(db, username, email, password, role)
        if user:
            # Automatically log in the user by creating and setting a token
            payload = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
            }
            token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
            response = make_response(jsonify({"message": "User created successfully", "role": user.role}), 201)
            response.set_cookie(
                'access_token',
                value=token,
                httponly=True,
                secure=os.getenv('FLASK_ENV') != 'development', # Set to True in production
                samesite='Lax',
                expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXP_DELTA_SECONDS)
            )
            return response
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({"error": f"Signup failed: {str(e)}"}), 500

def logout():
    """Logs the user out by clearing the access_token cookie."""
    try:
        response = make_response(jsonify({"message": "Logout successful"}), 200)
        response.set_cookie('access_token', '', expires=0, httponly=True)
        return response
    except Exception as e:
        return jsonify({"error": f"Logout failed: {str(e)}"}), 500
