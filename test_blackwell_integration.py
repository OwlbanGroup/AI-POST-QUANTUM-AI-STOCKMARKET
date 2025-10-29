#!/usr/bin/env python3
"""Test script for Blackwell TensorRT integration."""

import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai_model.predictive_model import PredictiveModel

def test_basic_functionality():
    """Test basic model functionality."""
    print("Testing basic model functionality...")

    # Create sample data
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = np.random.randn(100)

    # Test different model types
    for model_type in ['linear', 'random_forest', 'xgboost', 'ensemble']:
        print(f"\nTesting {model_type} model...")

        try:
            model = PredictiveModel(model_type=model_type, version='test-1.0')

            # Train model
            success = model.train(X, y)
            if not success:
                print(f"  ❌ Training failed for {model_type}")
                continue

            print(f"  ✅ Training successful for {model_type}")

            # Test prediction
            X_test = np.random.randn(10, 5)
            result = model.predict(X_test)

            if 'error' in result:
                print(f"  ❌ Prediction failed for {model_type}: {result['error']}")
            else:
                print(f"  ✅ Prediction successful for {model_type}")
                print(f"     Predictions shape: {result['predictions'].shape}")
                print(f"     Confidence shape: {result['confidence'].shape}")

            # Test evaluation
            eval_result = model.evaluate_model(X_test, np.random.randn(10))
            if 'error' in eval_result:
                print(f"  ❌ Evaluation failed for {model_type}: {eval_result['error']}")
            else:
                print(f"  ✅ Evaluation successful for {model_type}")
                print(f"     MSE: {eval_result.get('mse', 'N/A'):.4f}")

        except (ValueError, TypeError, RuntimeError) as e:
            print(f"  ❌ Exception in {model_type}: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected exception in {model_type}: {e}")

def test_tensorrt_optimization():
    """Test TensorRT optimization (mock test since we don't have actual models)."""
    print("\nTesting TensorRT optimization detection...")

    try:
        model = PredictiveModel(model_type='linear', version='test-1.0')

        # Check TensorRT availability
        from ai_model.predictive_model import TENSORRT_ENABLED, BLACKWELL_SUPPORTED
        print(f"  TensorRT enabled: {TENSORRT_ENABLED}")
        print(f"  Blackwell supported: {BLACKWELL_SUPPORTED}")

        # Test optimization method (will likely fail without actual model file)
        result = model.optimize_with_tensorrt("dummy_model_path")
        if result:
            print("  ✅ TensorRT optimization successful")
        else:
            print("  ❌ TensorRT optimization failed (expected without actual model)")

    except (ValueError, TypeError, RuntimeError) as e:
        print(f"  ❌ TensorRT test failed: {e}")
    except Exception as e:
        print(f"  ❌ Unexpected TensorRT test error: {e}")

def test_save_load():
    """Test model save and load functionality."""
    print("\nTesting model save/load...")

    try:
        model = PredictiveModel(model_type='linear', version='test-1.0')

        # Train briefly
        X = np.random.randn(50, 3)
        y = np.random.randn(50)
        model.train(X, y)

        # Save model
        filepath = "test_model.pkl"
        success = model.save_model(filepath)
        if success:
            print("  ✅ Model save successful")
        else:
            print("  ❌ Model save failed")
            return

        # Load model
        loaded_model = PredictiveModel.load_model(filepath)
        print("  ✅ Model load successful")

        # Test prediction with loaded model
        X_test = np.random.randn(5, 3)
        result = loaded_model.predict(X_test)
        if 'error' in result:
            print(f"  ❌ Loaded model prediction failed: {result['error']}")
        else:
            print("  ✅ Loaded model prediction successful")

        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

    except (ValueError, TypeError, RuntimeError) as e:
        print(f"  ❌ Save/load test failed: {e}")
    except Exception as e:
        print(f"  ❌ Unexpected save/load test error: {e}")

if __name__ == "__main__":
    print("Starting Blackwell TensorRT Integration Tests")
    print("=" * 50)

    test_basic_functionality()
    test_tensorrt_optimization()
    test_save_load()

    print("\n" + "=" * 50)
    print("Testing completed!")
