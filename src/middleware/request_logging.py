import logging
from flask import request

def log_request(response):
    logging.info(f"{request.method} {request.path} - {response.status}")
    return response

def setup_logging(app):
    logging.basicConfig(level=logging.INFO)
    app.after_request(log_request)
