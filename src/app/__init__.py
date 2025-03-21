from flask import Flask, Blueprint, jsonify, render_template
from flask_login import LoginManager  # Import Flask-Login
from src.app.auth import auth_bp  # Import the authentication blueprint

login_manager = LoginManager()  # Initialize the LoginManager
from src.middleware.request_logging import setup_logging  # Import the logging middleware
from src.middleware.request_logging import setup_logging  # Import the logging middleware

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/status')
def status():
    return jsonify({"status": "running"}), 200

from src.utils.swagger import swagger_bp  # Import the Swagger blueprint

app.register_blueprint(main_bp)  # Register the main Blueprint
app.register_blueprint(auth_bp)  # Register the authentication Blueprint
app.register_blueprint(swagger_bp)  # Register the Swagger Blueprint

@app.route('/')
def home():
    return render_template('index.html')

setup_logging(app)  # Set up the logging middleware

setup_logging(app)  # Set up the logging middleware

setup_logging(app)  # Set up the logging middleware
login_manager.init_app(app)  # Initialize Flask-Login with the app

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
