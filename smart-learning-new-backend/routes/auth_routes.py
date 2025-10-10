from flask import Blueprint
from auth.jwt_auth import login, signup

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    User Login.
    Authenticates a user and returns a JWT access token.
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
        description: Login successful, returns access token.
      401:
        description: Invalid credentials.
    """
    return login()

@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    """
    User Signup.
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
    return signup()
