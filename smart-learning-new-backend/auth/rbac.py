from functools import wraps
from flask import jsonify, g, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from user_service.service import UserService
from utils.database import get_db

def login_required(f): # This decorator now handles OPTIONS requests correctly
    # It's better to apply @jwt_required() inside the decorator to control the flow
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Bypass all checks for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return current_app.make_default_options_response()

        verify_jwt_in_request()
        try:
            db = next(get_db())
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
        # This decorator now correctly uses the logic from login_required
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = g.user
            if user.role not in allowed_roles:
                return jsonify({"status": "error", "message": "Access denied"}), 403
            return f(*args, **kwargs) # g.db is still available here
        return wrapper
    return decorator
