import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, Blueprint, jsonify, render_template
from flask_login import LoginManager  # Import Flask-Login
from app.auth import auth_bp  # Import the authentication blueprint

login_manager = LoginManager()  # Initialize the LoginManager
from middleware.request_logging import setup_logging  # Import the logging middleware

main_bp = Blueprint('main', __name__)

@main_bp.route('/status')
def status():
    return jsonify({"status": "running"}), 200

from utils.swagger import swagger_bp  # Import the Swagger blueprint
