from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to your Swagger JSON file

swagger_bp = Blueprint('swagger', __name__, url_prefix=SWAGGER_URL)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)

swagger_bp.register_blueprint(swaggerui_blueprint)
