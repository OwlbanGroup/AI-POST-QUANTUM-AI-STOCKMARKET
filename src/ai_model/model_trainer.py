from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from .model import StockMarketModel

class ModelTrainer:
    def __init__(self, model_type='linear'):
        self.model = StockMarketModel(model_type)

    def train(self, X, y):
        """Train the model and return evaluation metrics."""
        score = self.model.train(X, y)
        return score

    def evaluate(self, X_test, y_test):
        """Evaluate the model's performance using various metrics."""
        predictions = self.model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average='weighted'),
            "recall": recall_score(y_test, predictions, average='weighted'),
            "f1": f1_score(y_test, predictions, average='weighted')
        }
        return metrics
