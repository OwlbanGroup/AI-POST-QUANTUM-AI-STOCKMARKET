import pandas as pd
from .model import StockMarketModel

class ModelTrainer:
    def __init__(self, data):
        self.data = data
        self.model = StockMarketModel()

    def prepare_data(self):
        # Assuming 'target' is the column we want to predict
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        return X, y

    def train_model(self):
        X, y = self.prepare_data()
        score = self.model.train(X, y)
        return score
