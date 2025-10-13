"""
Main application file for the Smart Learning Platform.
"""
import logging
import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask import Flask, jsonify, g
from flask_cors import CORS
from flasgger import Swagger
from sqlalchemy.exc import OperationalError

# Load environment variables from .env as early as possible
load_dotenv()

from auth.rbac import role_required
from course_service.service import CourseService
from middleware.analytics_guard import analytics_guard_middleware
from middleware.logging_middleware import log_request_middleware
from middleware.rate_limiter import rate_limiter_middleware
from routes.admin_routes import admin_bp
from routes.analytics_routes import analytics_bp
from routes.assignment_routes import assignment_bp
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.dashboard_routes import dashboard_bp
from routes.user_routes import user_bp
from utils.database import Base, engine, get_db
from utils.seed_data import seed_users


app = Flask(__name__)

# --- JWT Configuration (using flask-jwt-extended) ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "a_very_strong_and_secret_key")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Expect JWTs in cookies

# In a real production app, this should be True!
# But for local development over HTTP, it must be False.
app.config["JWT_COOKIE_SECURE"] = os.getenv('FLASK_ENV') != 'development' 

# Set SameSite to 'None' to allow cross-origin cookie sending (e.g., from localhost:5173 to localhost:5000)
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"  # Explicitly set the cookie name
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Set to True for better security if needed

jwt = JWTManager(app)



swagger = Swagger(app)

# --- Swagger Configuration ---
app.config['SWAGGER'] = {
    'title': 'Smart Learning Platform API',
    'uiversion': 3,
    "specs_route": "/apidocs/"
}

# The root logger is now configured in the middleware, so we can let Werkzeug log to the console.
# log = logging.getLogger('werkzeug')
# log.disabled = True

# Register Middleware
log_request_middleware(app)
analytics_guard_middleware(app)
rate_limiter_middleware(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(course_bp, url_prefix="/api/courses")
app.register_blueprint(assignment_bp, url_prefix="/api/assignments")
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(dashboard_bp, url_prefix="/api")

# Initialize CORS after all blueprints are registered
CORS(app,
     origins=['http://127.0.0.1:5173', 'http://localhost:5173'],  # Your frontend URL
     supports_credentials=True,  # 🔥 Allow cookies
     allow_headers=['Content-Type', 'Authorization'],
     expose_headers=['Content-Type'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

@app.route("/")
def home():
    """
    Home route for the application.
    """
    return jsonify({"message": "Smart Learning Platform Auth Service Running"}), 200


# Dummy route for rate limiting test
@app.route("/recommendations", methods=["GET"])
@role_required(["student"])
def recommendations():
    """
    A real recommendation engine.
    Recommends courses the student is not currently enrolled in.
    """
    # Use the session from the decorator, to which the user object is already bound.
    db = g.db
    user = g.user

    # Get IDs of courses the user is enrolled in
    enrolled_course_ids = {enrollment.course_id for enrollment in user.enrollments}

    # Get all courses and filter out the ones the user is already in
    all_courses, _ = CourseService.get_all_courses(db, page=1, limit=100)

    recommended_courses = [
        {"id": c.id, "title": c.title, "description": c.description}
        for c in all_courses if c.id not in enrolled_course_ids
    ]
    return jsonify(recommended_courses)


@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables and seeds initial data."""
    try:
        print("[DB] Initializing database and creating tables...")
        Base.metadata.create_all(bind=engine)
        print("[DB] Database tables created/verified.")
        # Seed mock data from mock_data/users.json
        seed_users()
        print("[DB] Database initialization complete.")
    except (ValueError, OperationalError) as e:
        print("\n" + "=" * 60)
        print("FATAL: DATABASE INITIALIZATION FAILED".center(60))
        print("=" * 60)
        print(f"Error: {e}")
        print("\nPlease ensure your .env file is in the project root and contains:")
        print("  - MYSQL_USER=<your_username>")
        print("  - MYSQL_PASSWORD=<your_password>")
        print("  - MYSQL_DB=<your_database_name>")
        print("Also, ensure your MySQL server is running and accessible.")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    # Use 0.0.0.0 to make the server accessible externally (for cloud deployment).
    # The debug flag should be set to False in a production environment.
    app.run(host="0.0.0.0", debug=True)