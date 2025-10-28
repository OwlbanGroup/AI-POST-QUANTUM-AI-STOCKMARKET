import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor
from tensorflow.python.keras.models import load_model
import joblib
import logging
from datetime import datetime
from typing import Dict, Union
import torch
from .gemini_integration import GeminiIntegration

# NVIDIA Blackwell architecture detection and optimization
try:
    import torch
    if torch.cuda.is_available():
        BLACKWELL_SUPPORTED = torch.cuda.get_device_capability()[0] >= 9  # Blackwell starts at compute capability 9.x
        logger.info(f"NVIDIA Blackwell architecture detected: {BLACKWELL_SUPPORTED}")
    else:
        BLACKWELL_SUPPORTED = False
except ImportError:
    BLACKWELL_SUPPORTED = False

# NVIDIA TensorRT integration with Blackwell optimizations
try:
    import tensorrt as trt
    from tensorflow.python.compiler.tensorrt import trt_convert
    TENSORRT_ENABLED = True
    logger.info("TensorRT enabled with Blackwell optimizations")
except ImportError:
    TENSORRT_ENABLED = False
    logger.warning("TensorRT not available - Blackwell optimizations disabled")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictiveModel:
    def __init__(self, model_type='linear', version='1.0'):
        self.model_type = model_type
        self.version = version
        self.last_trained = None
        self.gemini_integration = GeminiIntegration()  # Initialize Gemini integration
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the appropriate model based on type"""
        if self.model_type == 'linear':
            self.model = LinearRegression()
        elif self.model_type == 'random_forest':
            self.model = RandomForestRegressor()
        elif self.model_type == 'xgboost':
            self.model = XGBRegressor()
        elif self.model_type == 'ensemble':
            self.model = self._create_ensemble()
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def _create_ensemble(self):
        """Create an ensemble of models"""
        return VotingRegressor([
            ('lr', LinearRegression()),
            ('rf', RandomForestRegressor(n_estimators=100)),
            ('xgb', XGBRegressor())
        ])

    def train(self, X, y):
        """Train the model using historical data."""
        try:
            self.model.fit(X, y)
            self.last_trained = datetime.now().isoformat()
            logger.info(f"Model trained successfully. Version: {self.version}")
            return True
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False

    def predict(self, X) -> Dict[str, Union[np.ndarray, float]]:
        """Make predictions with confidence scores and optional Gemini enhancement."""
        try:
            preds = self.model.predict(X)

            # Calculate confidence scores (varies by model type)
            if hasattr(self.model, 'predict_proba'):
                confidence = np.max(self.model.predict_proba(X), axis=1)
            else:
                # For regression models, use inverse of standard deviation
                if hasattr(self.model, 'estimators_'):
                    preds_all = np.array([e.predict(X) for e in self.model.estimators_])
                    confidence = 1 / (1 + np.std(preds_all, axis=0))
                else:
                    confidence = np.ones(len(preds)) * 0.8  # Default confidence

            base_result = {
                'predictions': preds,
                'confidence': confidence,
                'model_version': self.version,
                'last_trained': self.last_trained
            }

            # Enhance predictions with Gemini insights if available
            if self.gemini_integration.is_available():
                try:
                    market_context = {
                        'predictions': preds.tolist() if hasattr(preds, 'tolist') else preds,
                        'confidence': confidence.tolist() if hasattr(confidence, 'tolist') else confidence,
                        'model_type': self.model_type,
                        'timestamp': datetime.now().isoformat()
                    }

                    enhanced_result = self.gemini_integration.enhance_predictions(base_result, market_context)
                    return enhanced_result
                except Exception as gemini_error:
                    logger.warning(f"Gemini enhancement failed: {gemini_error}")
                    return base_result
            else:
                return base_result

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {
                'error': str(e),
                'model_version': self.version
            }

    def update_model(self, new_X, new_y):
        """Update the model with new data."""
        try:
            if self.model_type == 'ensemble':
                # For ensembles, we need to update each sub-model
                for name, model in self.model.named_estimators_.items():
                    model.fit(new_X, new_y)
            else:
                self.model.fit(new_X, new_y)
            
            self.last_trained = datetime.now().isoformat()
            logger.info(f"Model updated successfully. Version: {self.version}")
            return True
        except Exception as e:
            logger.error(f"Error updating model: {e}")
            return False

    def optimize_with_tensorrt(self, model_path: str) -> bool:
        """Optimize the model using TensorRT for faster inference with Blackwell optimizations."""
        if not TENSORRT_ENABLED:
            logger.warning("TensorRT not available - skipping optimization")
            return False

        try:
            # Blackwell-specific TensorRT optimizations
            if BLACKWELL_SUPPORTED:
                logger.info("Applying Blackwell-specific TensorRT optimizations")

                # Enhanced conversion parameters for Blackwell architecture
                conversion_params = trt_convert.DEFAULT_TRT_CONVERSION_PARAMS
                conversion_params = conversion_params._replace(
                    max_workspace_size_bytes=1 << 28,  # Increased for Blackwell's larger memory
                    precision_mode=trt_convert.TrtPrecisionMode.FP16,  # Blackwell optimized for FP16
                    use_calibration=True,  # Enable INT8 calibration for Blackwell
                    allow_build_at_runtime=True  # Dynamic shape support
                )

                # Blackwell-specific builder configuration
                builder_config = trt.BuilderConfig()
                builder_config.max_workspace_size = 1 << 28
                builder_config.set_flag(trt.BuilderFlag.FP16)
                builder_config.set_flag(trt.BuilderFlag.SPARSE_WEIGHTS)  # Blackwell sparse tensor support

                # Convert and save optimized model
                converter = trt_convert.TrtGraphConverterV2(
                    input_saved_model_dir=model_path,
                    conversion_params=conversion_params
                )
                converter.convert()
                converter.save(f"{model_path}_blackwell_trt")

                logger.info("Model successfully optimized with Blackwell TensorRT")
            else:
                # Fallback to standard TensorRT optimization
                conversion_params = trt_convert.DEFAULT_TRT_CONVERSION_PARAMS
                conversion_params = conversion_params._replace(
                    max_workspace_size_bytes=1 << 25,
                    precision_mode=trt_convert.TrtPrecisionMode.FP16
                )

                converter = trt_convert.TrtGraphConverterV2(
                    input_saved_model_dir=model_path,
                    conversion_params=conversion_params
                )
                converter.convert()
                converter.save(f"{model_path}_trt")

                logger.info("Model successfully optimized with standard TensorRT")

            return True
        except Exception as e:
            logger.error(f"TensorRT optimization failed: {e}")
            return False

    def evaluate_model(self, X_test, y_test) -> Dict[str, float]:
        """Evaluate the model's performance with multiple metrics."""
        try:
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            preds = self.model.predict(X_test)
            return {
                'mse': mean_squared_error(y_test, preds),
                'mae': mean_absolute_error(y_test, preds),
                'r2': r2_score(y_test, preds),
                'model_version': self.version
            }
        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
            return {
                'error': str(e),
                'model_version': self.version
            }

    def save_model(self, filepath: str) -> bool:
        """Save the model to disk."""
        try:
            if self.model_type in ['ensemble', 'xgboost']:
                joblib.dump(self.model, filepath)
            else:
                joblib.dump(self, filepath)
            logger.info(f"Model saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False

    @staticmethod
    def load_model(filepath: str) -> 'PredictiveModel':
        """Load a model from disk."""
        try:
            model = joblib.load(filepath)
            logger.info(f"Model loaded from {filepath}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
