from flask import Flask
from data.data_loader import DataLoader
from data.data_preprocessing import DataPreprocessor
from ai_model.training import ModelTrainer

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Stock Market Application!"

@app.route('/train_model')
def train_model():
    # Load and preprocess data
    data_loader = DataLoader('path_to_your_data.csv')
    data = data_loader.load_data()
    
    preprocessor = DataPreprocessor(data)
    processed_data = preprocessor.preprocess()
    
    trainer = ModelTrainer(processed_data)
    score = trainer.train_model()
    
    return f"Model trained with score: {score}"

if __name__ == "__main__":
    app.run(debug=True)
