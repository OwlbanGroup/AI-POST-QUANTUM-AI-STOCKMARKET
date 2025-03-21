from flask import Flask, Blueprint
from sentry_sdk import init

# Initialize Sentry
init(dsn="your_sentry_dsn_here")

from src.utils.error_handling import handle_error

app = Flask(__name__)
app.register_error_handler(Exception, handle_error)
from src.utils.logger import setup_logger

logger = setup_logger()

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    logger.info("Starting the application with error handling and Sentry monitoring...")
    app.run(debug=False, host='0.0.0.0', port=5000)
