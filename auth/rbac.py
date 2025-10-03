from functools import wraps
from flask import request, jsonify, g
import jwt
from utils.config import Config
from user_service.service import UserService
from utils.database import get_db

def _get_user_from_token(db):
    """Helper function to decode token, retrieve user, and handle errors."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Authorization header is missing or malformed"}), 401)

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        # The database session should be handled by the route's context
        user = UserService.get_user_by_id(db, payload['id'])
        if not user:
            return None, (jsonify({"error": "User not found"}), 404)
        return user, None
    except jwt.ExpiredSignatureError:
        return None, (jsonify({"error": "Token has expired"}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({"error": "Invalid token"}), 401)
    except Exception as e:
        # Log the actual error for debugging
        # logging.error(f"Token processing error: {e}")
        return None, (jsonify({"error": "An error occurred while processing the token"}), 401)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = next(get_db())
        user, error_response = _get_user_from_token(db)
        if error_response:
            return error_response
        g.user = user  # Attach user to Flask's global context
        # Note: The user object is attached to the session 'db'
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required  # Reuse the login_required decorator to get the user
        def wrapper(*args, **kwargs):
            user = g.user  # g.user is now set by @login_required

            if user.role not in allowed_roles:
                return jsonify({"error": "Access denied. You do not have the required role."}), 403

            # Pass the user object to the decorated function
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
