from flask import Flask, render_template
from src.data.real_time_data import RealTimeData

class UserInterface:
    def __init__(self, app):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/real_time/<ticker>')
        def real_time(ticker):
            data_handler = RealTimeData(ticker)
            data = data_handler.fetch_real_time_data()
            processed_data = data_handler.process_data(data)
            return render_template('real_time.html', data=processed_data)

# Initialize Flask app
app = Flask(__name__)
ui = UserInterface(app)

if __name__ == '__main__':
    app.run(debug=True)
