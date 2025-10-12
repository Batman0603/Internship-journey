from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from user_service.service import UserService
from utils.database import get_db

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        g.db = next(get_db())
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(g.db, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        g.user = user
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            g.db = next(get_db())
            user_id = get_jwt_identity()
            user = UserService.get_user_by_id(g.db, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            if user.role not in allowed_roles:
                return jsonify({"error": "Access denied. You do not have the required role."}), 403

            # Pass the user object to the decorated function
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
