from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    description: Create a new user account with a username and password.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: johndoe
              password:
                type: string
                example: mysecurepassword
    responses:
      201:
        description: User created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User created successfully
      400:
        description: Username already exists
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Username already exists
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    if User.objects(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    user.save()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    description: Log in a registered user and return a JWT access token.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: johndoe
              password:
                type: string
                example: mysecurepassword
    responses:
      200:
        description: Successfully logged in and returns JWT token
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Invalid credentials
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Invalid credentials
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200
