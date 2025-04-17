import numpy as np
from src.ai_model.predictive_model import PredictiveModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_predictive_model():
    """Comprehensive test for PredictiveModel functionality."""
    try:
        # Generate sample data
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y = np.array([1, 2, 3, 4])
        test_X = np.array([[5, 6]])

        # Test different model types
        for model_type in ['linear', 'random_forest', 'xgboost']:
            logger.info(f"\nTesting {model_type} model...")
            
            # Initialize and train
            model = PredictiveModel(model_type=model_type)
            assert model.train(X, y), "Training failed"
            
            # Make prediction
            result = model.predict(test_X)
            assert 'predictions' in result, "Prediction failed"
            logger.info(f"Predictions: {result['predictions']}")
            
            # Verify confidence scores
            assert 'confidence' in result, "Missing confidence scores"
            logger.info(f"Confidence: {result['confidence']}")
            
            # Test model updating
            assert model.update_model(X, y), "Model update failed"
            
            logger.info(f"{model_type} model tests passed")

        logger.info("All model tests completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_predictive_model()
    if success:
        print("All tests passed successfully")
    else:
        print("Some tests failed")
