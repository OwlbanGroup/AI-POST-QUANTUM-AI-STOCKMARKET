from flask import Flask, Blueprint

app = Flask(__name__)
main_bp = Blueprint('main', __name__)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
