from flask import Blueprint
from auth.jwt_auth import handle_login, handle_signup, handle_logout

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    User Login.
    User login route.
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
            password:
              type: string
              format: password
    responses:
      200:
        description: Login successful.
      401:
        description: Unauthorized.
    """
    return handle_login()

@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    """
    Registers a new user in the system.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
            email:
              type: string
              format: email
            password:
              type: string
              format: password
    responses:
      201:
        description: User created successfully.
      409:
        description: User with this email already exists.
    """
    return handle_signup()

@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    """
    Logs the user out by clearing the access_token cookie.
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Logout successful.
      500:
        description: Logout failed.
    """
    return handle_logout()
