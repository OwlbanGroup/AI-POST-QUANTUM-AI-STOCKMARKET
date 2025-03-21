import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from post_quantum_library import PostQuantumRegressor

class StockMarketModel:
    def __init__(self):
        self.model = PostQuantumRegressor()

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        return self.model.score(X_test, y_test)

    def predict(self, X):
        return self.model.predict(X)
