from functools import wraps
from flask import request, jsonify, g
import jwt
from utils.config import Config
from user_service.service import UserService

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"error": "Malformed token"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            user = UserService.get_user_by_id(payload['id'])
            if not user:
                return jsonify({"error": "User not found"}), 404
            g.user = user # Attach user to Flask's global context
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                try:
                    token = request.headers.get("Authorization").split(" ")[1]
                except IndexError:
                    return jsonify({"error": "Malformed token"}), 401
            if not token:
                return jsonify({"error": "Token missing"}), 401
            try:
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                if payload['role'] not in allowed_roles:
                    return jsonify({"error": "Access denied"}), 403
                user = UserService.get_user_by_id(payload['id'])
                if not user:
                    return jsonify({"error": "User not found"}), 404
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
