import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.ai_model.federated_learning import FederatedLearning


class TestFederatedLearning:
    """Test cases for Federated Learning implementation."""

    def test_federated_averaging_basic(self):
        """Test basic federated averaging functionality."""
        fl = FederatedLearning()
        
        # Create sample model updates
        updates = [
            {'weight': np.array([1.0, 2.0]), 'bias': np.array([0.1])},
            {'weight': np.array([3.0, 4.0]), 'bias': np.array([0.2])},
            {'weight': np.array([5.0, 6.0]), 'bias': np.array([0.3])}
        ]
        
        result = fl.federated_averaging(updates)
        
        # Verify averaging
        expected_weight = np.array([3.0, 4.0])  # (1+3+5)/3, (2+4+6)/3
        expected_bias = np.array([0.2])  # (0.1+0.2+0.3)/3
        
        assert np.allclose(result['weight'], expected_weight)
        assert np.allclose(result['bias'], expected_bias)

    def test_federated_averaging_weighted(self):
        """Test weighted federated averaging."""
        fl = FederatedLearning()
        
        updates = [
            {'param': np.array([1.0, 2.0])},
            {'param': np.array([3.0, 4.0])}
        ]
        weights = [0.7, 0.3]
        
        result = fl.federated_averaging(updates, weights)
        
        expected = np.array([1.0*0.7 + 3.0*0.3, 2.0*0.7 + 4.0*0.3])
        assert np.allclose(result['param'], expected)

    def test_secure_aggregation_with_encryption(self):
        """Test secure aggregation with encryption."""
        fl = FederatedLearning()
        
        updates = [
            {'param': np.array([1.0, 2.0])},
            {'param': np.array([3.0, 4.0])}
        ]
        secret_key = "test-secret-key"
        
        result = fl.secure_aggregation(updates, secret_key)
        
        # Should get the average of [1,2] and [3,4] = [2,3]
        expected = np.array([2.0, 3.0])
        assert np.allclose(result['param'], expected)

    def test_secure_aggregation_without_encryption(self):
        """Test secure aggregation without encryption (fallback)."""
        fl = FederatedLearning()
        
        updates = [
            {'param': np.array([1.0, 2.0])},
            {'param': np.array([3.0, 4.0])}
        ]
        
        result = fl.secure_aggregation(updates)
        
        expected = np.array([2.0, 3.0])
        assert np.allclose(result['param'], expected)

    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption and decryption roundtrip."""
        fl = FederatedLearning()
        
        original_update = {'param': np.array([1.0, 2.0, 3.0])}
        secret_key = "test-secret-key"
        
        encrypted = fl._encrypt_update(original_update, secret_key)
        decrypted = fl._decrypt_update(encrypted, secret_key)
        
        assert np.allclose(original_update['param'], decrypted['param'])

    @patch('src.ai_model.federated_learning.Workspace', create=True)
    @patch('src.ai_model.federated_learning.Experiment', create=True)
    def test_azure_ml_integration_success(self, mock_experiment, mock_workspace):
        """Test successful Azure ML integration."""
        mock_ws_instance = MagicMock()
        mock_workspace.get.return_value = mock_ws_instance
        
        mock_exp_instance = MagicMock()
        mock_experiment.return_value = mock_exp_instance
        
        fl = FederatedLearning(azure_ml_workspace="test-workspace")
        
        mock_workspace.get.assert_called_once_with(name="test-workspace")
        mock_experiment.assert_called_once_with(
            workspace=mock_ws_instance, name='federated-learning'
        )
        # Use fl to avoid unused variable warning
        assert fl.azure_ml_workspace == "test-workspace"
    
    def test_azure_ml_integration_failure(self):
        """Test Azure ML integration failure."""
        # This test doesn't need mocking since ImportError will be caught
        fl = FederatedLearning(azure_ml_workspace="test-workspace")
        
        # Should handle ImportError gracefully - workspace should be None
        # since Azure ML SDK is not actually installed
        assert fl.workspace is None
    
    @patch('src.ai_model.federated_learning.Run', create=True)
    def test_azure_ml_log_metrics_success(self, mock_run):
        """Test successful Azure ML metrics logging."""
        mock_run_instance = MagicMock()
        mock_run.get_context.return_value = mock_run_instance
        
        fl = FederatedLearning(azure_ml_workspace="test-workspace")
        # Mock the workspace to simulate Azure ML being available
        fl.workspace = MagicMock()
        
        metrics = {'accuracy': 0.95, 'loss': 0.1}
        fl.azure_ml_log_metrics(metrics)
        
        # Should log locally since Azure ML SDK is not actually available
        # The test verifies the method doesn't crash
        
    def test_azure_ml_log_metrics_no_workspace(self):
        """Test metrics logging without Azure ML workspace."""
        fl = FederatedLearning()  # No workspace provided
        
        metrics = {'accuracy': 0.95, 'loss': 0.1}
        
        # Should log locally without error
        fl.azure_ml_log_metrics(metrics)

    def test_empty_updates_error(self):
        """Test error handling for empty updates."""
        fl = FederatedLearning()
        
        error_msg = "No updates provided for aggregation"
        with pytest.raises(ValueError, match=error_msg):
            fl.federated_averaging([])

    def test_mismatched_weights_error(self):
        """Test error handling for mismatched weights and updates."""
        fl = FederatedLearning()
        
        updates = [{'param': np.array([1.0])}, {'param': np.array([2.0])}]
        weights = [0.5]  # Only one weight for two updates
        
        error_msg = "Number of weights must match number of updates"
        with pytest.raises(ValueError, match=error_msg):
            fl.federated_averaging(updates, weights)
        
    def test_model_parameters_storage(self):
        """Test that model parameters are stored correctly."""
        fl = FederatedLearning()
        
        assert fl.get_model_parameters() is None
        
        new_params = {'weight': np.array([1.0]), 'bias': np.array([0.1])}
        fl.update_model(new_params)
        
        assert fl.get_model_parameters() == new_params

    def test_aggregate_updates_backward_compatibility(self):
        """Test backward compatibility method."""
        fl = FederatedLearning()
        
        updates = [
            {'param': np.array([1.0, 2.0])},
            {'param': np.array([3.0, 4.0])}
        ]
        
        result = fl.aggregate_updates(updates)
        expected = np.array([2.0, 3.0])
        
        assert np.allclose(result['param'], expected)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
