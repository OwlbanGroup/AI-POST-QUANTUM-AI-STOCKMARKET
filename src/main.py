from flask import Flask, Blueprint
from src.utils.logger import setup_logger

logger = setup_logger()

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    logger.info("Starting the application...")
    app.run(debug=False, host='0.0.0.0', port=5000)
