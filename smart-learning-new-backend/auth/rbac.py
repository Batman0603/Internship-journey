from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from user_service.service import UserService
from utils.database import get_db

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        db = next(get_db())
        try:
            user_id = get_jwt_identity()
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404
            g.user = user
            g.db = db
            return f(*args, **kwargs)
        finally:
            db.close()  # ✅ ensures DB session is closed
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            user = g.user
            if user.role not in allowed_roles:
                return jsonify({"status": "error", "message": "Access denied"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
