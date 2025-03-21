from flask import Flask
from data.data_loader import DataLoader
from data.data_preprocessing import DataPreprocessor
from ai_model.training import ModelTrainer

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Stock Market Application! Use /train_model to train the model."

@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    # Load and preprocess data from a CSV file
    data_loader = DataLoader('src/data/sample_data.csv')  # Updated to use the sample data file
    data = data_loader.load_data()
    
    preprocessor = DataPreprocessor(data)
    processed_data = preprocessor.preprocess()
    
    trainer = ModelTrainer(processed_data)
    score = trainer.train_model()
    
    return f"Model trained with score: {score}"

if __name__ == "__main__":
    app.run(debug=True)
