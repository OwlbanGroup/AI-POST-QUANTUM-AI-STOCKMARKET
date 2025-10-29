import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from app import main_bp  # Import the main_bp from app

app = Flask(__name__)

app.register_blueprint(main_bp)  # Register the Blueprint

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
