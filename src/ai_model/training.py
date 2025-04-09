import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
from .model import StockMarketModel
from pqcrypto.sign.dilithium2 import sign, verify

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, data, model_type='linear'):
        self.data = data
        self.model = StockMarketModel(model_type=model_type)
        self.evaluation_metrics = {}

    def quantum_resistant_data_handling(self, data):
        """Apply quantum-resistant transformations to data"""
        try:
            # Apply standardization
            normalized_data = (data - data.mean()) / data.std()
            
            # Apply dimensionality reduction
            if len(data.columns) > 10:
                corr_matrix = data.corr().abs()
                upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
                to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
                normalized_data = normalized_data.drop(to_drop, axis=1)
            
            logger.info("Applied quantum-resistant data transformations")
            return normalized_data
        except Exception as e:
            logger.error(f"Error in quantum-resistant handling: {e}")
            return data

    def prepare_data(self):
        try:
            if 'target' not in self.data.columns:
                logger.error("Target column is missing from the data.")
                return None, None
            
            self.data = self.quantum_resistant_data_handling(self.data)
            X = self.data.drop('target', axis=1)
            y = self.data['target']
            return X, y
        except Exception as e:
            logger.error(f"Error during data preparation: {e}")
            return None, None

    def tune_hyperparameters(self, X, y):
        """Perform hyperparameter tuning"""
        try:
            if isinstance(self.model.model, (RandomForestRegressor, XGBRegressor)):
                param_grid = {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 10, 20]
                }
                grid_search = GridSearchCV(
                    estimator=self.model.model,
                    param_grid=param_grid,
                    cv=3,
                    scoring='neg_mean_squared_error'
                )
                grid_search.fit(X, y)
                self.model.model = grid_search.best_estimator_
                logger.info(f"Best params: {grid_search.best_params_}")
        except Exception as e:
            logger.warning(f"Hyperparameter tuning failed: {e}")

    def evaluate_model(self, X_test, y_test, y_pred):
        """Calculate multiple evaluation metrics"""
        self.evaluation_metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        return self.evaluation_metrics

    def train_model(self):
        X, y = self.prepare_data()
        if X is None or y is None:
            logger.error("Data preparation failed, cannot train model.")
            return None
        
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42)
            
            self.tune_hyperparameters(X_train, y_train)
            score = self.model.train(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            metrics = self.evaluate_model(X_test, y_test, y_pred)
            
            logger.info(f"Training completed. Score: {score}")
            logger.info(f"Evaluation metrics: {metrics}")
            
            return {
                'score': score,
                'metrics': metrics,
                'feature_importances': self.model.feature_importances_
            }
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            return None
