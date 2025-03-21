from flask import Flask, request, jsonify
from src.data.data_loader import DataLoader
from src.data.data_preprocessing import DataPreprocessor
from src.ai_model.training import ModelTrainer

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Stock Market Application! Use /train_model to train the model."

@app.route('/place_order', methods=['POST'])
def place_order():
    # Logic to place an order
    order_data = request.json
    trading_engine.place_order(order_data['type'], order_data['amount'], order_data['price'])
    return jsonify({"message": "Order placed successfully!"})

@app.route('/execute_trades', methods=['POST'])
def execute_trades():
    trading_engine.execute_trades()
    return jsonify({"message": "Trades executed successfully!"})

@app.route('/get_orders', methods=['GET'])
def get_orders():
    orders = trading.get_orders()
    return jsonify(orders)

@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    # Load and preprocess data from a CSV file
    data_loader = DataLoader('src/data/sample_data.csv')  # Updated to use the sample data file
    data = data_loader.load_data()
    
    preprocessor = DataPreprocessor(data)
    processed_data = preprocessor.preprocess()
    print("Loaded Data:", processed_data)  # Debugging statement to check loaded data
    preprocessor.print_data_types()  # Print data types after preprocessing
    
    trainer = ModelTrainer(processed_data)
    score = trainer.train_model()
    
    return f"Model trained with score: {score}"

if __name__ == "__main__":
    app.run(debug=True)
