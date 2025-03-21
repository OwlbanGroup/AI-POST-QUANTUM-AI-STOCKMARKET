from flask import jsonify

def handle_error(e):
    """Handle errors and return a JSON response."""
    response = {
        "error": str(e),
        "message": "An error occurred. Please try again."
    }
    return jsonify(response), 500
