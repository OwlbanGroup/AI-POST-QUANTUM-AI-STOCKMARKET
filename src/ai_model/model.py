import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
try:
    import tensorflow as tf
    from tensorflow.python.keras.models import Sequential
    from tensorflow.python.keras.layers import LSTM, Dense
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
try:
    from pqcrypto.sign.dilithium2 import keypair, sign, verify
    PQCRYPTO_AVAILABLE = True
except ImportError:
    PQCRYPTO_AVAILABLE = False
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockMarketModel:
    def __init__(self, model_type='linear'):
        self.model_type = model_type
        self.feature_importances_ = None
        self.post_quantum_key = None
        
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor()
        elif model_type == 'xgboost':
            self.model = XGBRegressor()
        elif model_type == 'lstm':
            self.model = self._build_lstm_model()
        elif model_type == 'post_quantum':
            self.model = LinearRegression()  # Placeholder for actual PQ model
            self._generate_pq_keys()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def _build_lstm_model(self):
        if not TENSORFLOW_AVAILABLE:
            raise ImportError(
                "TensorFlow is required for LSTM models but not available. "
                "Please install tensorflow or choose a different model type."
            )
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(1, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model
        
    def _generate_pq_keys(self):
        """Generate post-quantum cryptographic keys"""
        if not PQCRYPTO_AVAILABLE:
            raise ImportError(
                "pqcrypto is required for post-quantum features but not available. "
                "Please install pqcrypto or choose a different model type."
            )
        try:
            self.post_quantum_key = keypair()
            logger.info("Generated post-quantum keys")
        except Exception as e:
            logger.error(f"Error generating PQ keys: {e}")
        
    def train(self, X, y):
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42)
            
            if self.model_type == 'lstm':
                X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
                X_test = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))
                self.model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
            else:
                self.model.fit(X_train, y_train)
            
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importances_ = self.model.feature_importances_
            
            score = self.model.score(X_test, y_test)
            logger.info(f"Model training completed with score: {score}")
            return score
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return None

    def predict(self, X):
        try:
            if self.model_type == 'lstm':
                X = X.values.reshape((X.shape[0], 1, X.shape[1]))
            return self.model.predict(X)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return None

    def save_model(self, filepath):
        """Save model to file using joblib"""
        try:
            joblib.dump(self.model, filepath)
            logger.info(f"Model saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False

    def load_model(self, filepath):
        """Load model from file using joblib"""
        try:
            self.model = joblib.load(filepath)
            logger.info(f"Model loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
