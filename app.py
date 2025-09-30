from flask import Flask, jsonify
import sys
from dotenv import load_dotenv # Moved to the top

# Load environment variables from .env as early as possible
load_dotenv()

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from user_service.models import Base
from utils.database import engine
from utils.seed_data import seed_users
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Create tables (ignore if already exist)
try:
    print("[DB] Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("[DB] Database tables created/verified.")
    # Seed mock data from mock_data/users.json
    seed_users()
except (ValueError, OperationalError) as e:
    print("\n" + "="*60)
    print("FATAL: DATABASE INITIALIZATION FAILED".center(60))
    print("="*60)
    print(f"Error: {e}")
    print("\nPlease ensure your .env file is in the project root and contains:")
    print("  - MYSQL_USER=<your_username>")
    print("  - MYSQL_PASSWORD=<your_password>")
    print("  - MYSQL_DB=<your_database_name>")
    print("Also, ensure your MySQL server is running and accessible.")
    print("="*60 + "\n")
    sys.exit(1) # Stop the application

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/admin")

@app.route("/")
def home():
    return jsonify({"message": "Smart Learning Platform Auth Service Running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
