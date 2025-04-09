import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor  # type: ignore # Example of an additional model type
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictiveModel:
    def __init__(self, model_type='linear'):
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor()
        else:
            raise ValueError("Unsupported model type")

    def train(self, X, y):
        """Train the model using historical data."""
        try:
            self.model.fit(X, y)
        except Exception as e:
            logger.error(f"Error during training: {e}")

    def predict(self, X):
        """Make predictions based on the input data."""
        try:
            return self.model.predict(X)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")

    def update_model(self, new_X, new_y):
        """Update the model with new data."""
        self.train(new_X, new_y)

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model's performance."""
        try:
            score = self.model.score(X_test, y_test)
            return score
        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
