from flask import request, jsonify
from utils.config import Config

def analytics_guard_middleware(app):
    @app.before_request
    def check_api_key():
        if request.path.startswith("/analytics"):
            api_key = request.args.get("apiKey")
            # Use an environment variable for the API key
            if not Config.ANALYTICS_API_KEY or api_key != Config.ANALYTICS_API_KEY:
                return jsonify({"error": "Forbidden. Invalid API key."}), 403
