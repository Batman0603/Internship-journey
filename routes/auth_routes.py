from flask import Blueprint
from auth.jwt_auth import login, signup

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()

@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    return signup()
