from functools import wraps
from flask import request, jsonify
import jwt
from utils.config import Config

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers.get("Authorization").split(" ")[1]
            if not token:
                return jsonify({"error": "Token missing"}), 401
            try:
                data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
                if data['role'] not in allowed_roles:
                    return jsonify({"error": "Access denied"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator
