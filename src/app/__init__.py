from flask import Flask, Blueprint, jsonify

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/status')
def status():
    return jsonify({"status": "running"}), 200

@main_bp.route('/status')
def status():
    return jsonify({"status": "running"}), 200

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
