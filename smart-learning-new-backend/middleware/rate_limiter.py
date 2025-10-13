import time
from flask import request, jsonify

user_requests = {}

def rate_limiter_middleware(app):
    @app.before_request
    def limit_requests():
        if request.path.startswith("/recommendations"):
            user_ip = request.remote_addr
            now = time.time()

            if user_ip not in user_requests:
                user_requests[user_ip] = []

            # Keep only requests from the last 60 seconds
            user_requests[user_ip] = [t for t in user_requests[user_ip] if now - t < 60]

            if len(user_requests[user_ip]) >= 10:
                return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

            user_requests[user_ip].append(now)
