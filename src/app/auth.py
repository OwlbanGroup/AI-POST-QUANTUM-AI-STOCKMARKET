"""Authentication blueprint for Flask-Login integration.

Handles user login and logout endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from models.user import User  # Import the User model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login() -> tuple[dict[str, str], int]:
    \"\"\"Handle user login via POST /login.

    Expects JSON: {"user_id": "some_id"}

    Returns:
        tuple: (JSON response, 200 status)
    \"\"\"
    user_id = request.json.get('user_id')
    user = User(user_id)
    login_user(user)
    return jsonify({"message": "Logged in successfully"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout() -> tuple[dict[str, str], int]:
    \"\"\"Handle user logout via POST /logout.

    Returns:
        tuple: (JSON response, 200 status)
    \"\"\"
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
