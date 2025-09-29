from flask import Flask, jsonify
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from user_service.models import Base
from utils.database import engine
from utils.seed_data import seed_users
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Create tables (ignore if already exist)
Base.metadata.create_all(bind=engine)

# Seed mock data from mock_data/users.json
seed_users()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/admin")

@app.route("/")
def home():
    return jsonify({"message": "Smart Learning Platform Auth Service Running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
