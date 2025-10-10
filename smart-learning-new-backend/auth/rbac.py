from functools import wraps
from flask import request, jsonify, g
import jwt
from utils.config import Config
from user_service.service import UserService
from utils.database import get_db

def _get_user_from_token(db):
    """Helper function to decode token, retrieve user, and handle errors."""
    token = request.cookies.get("access_token")

    if not token:
        return None, (jsonify({"error": "Authentication token is missing"}), 401)

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
        g.db = next(get_db())
        user, error_response = _get_user_from_token(g.db)
        if error_response:
            return error_response
        g.user = user  # Attach user to Flask's global context
        # The user object is attached to the session g.db
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required  # Reuse the login_required decorator to get the user
        def wrapper(*args, **kwargs):
            user = g.user  # g.user and g.db are now set by @login_required

            if user.role not in allowed_roles:
                return jsonify({"error": "Access denied. You do not have the required role."}), 403

            # Pass the user object to the decorated function
            return f(user, *args, **kwargs)
        return wrapper
    return decorator
