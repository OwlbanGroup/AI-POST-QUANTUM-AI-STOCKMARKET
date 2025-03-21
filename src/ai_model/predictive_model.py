import numpy as np
from sklearn.linear_model import LinearRegression

class PredictiveModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        """Train the model using historical data."""
        self.model.fit(X, y)

    def predict(self, X):
        """Make predictions based on the input data."""
        return self.model.predict(X)

    def update_model(self, new_X, new_y):
        """Update the model with new data."""
        self.train(new_X, new_y)
