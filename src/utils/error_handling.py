from flask import jsonify

def handle_error(error):
    response = {
        "error": str(error),
        "message": "An error occurred. Please check your request and try again."
    }
    return jsonify(response), 500
