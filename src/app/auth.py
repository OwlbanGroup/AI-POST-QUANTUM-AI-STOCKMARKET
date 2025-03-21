from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from src.models.user import User  # Import the User model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')
    user = User(user_id)
    login_user(user)
    return jsonify({"message": "Logged in successfully"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
