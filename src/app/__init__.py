from flask import Flask, Blueprint, jsonify

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/status')
def status():
    return jsonify({"status": "running"}), 200

from src.utils.swagger import swagger_bp  # Import the Swagger blueprint

app.register_blueprint(main_bp)  # Register the main Blueprint
app.register_blueprint(swagger_bp)  # Register the Swagger Blueprint

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
