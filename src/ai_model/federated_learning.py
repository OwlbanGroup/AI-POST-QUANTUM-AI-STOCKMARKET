import numpy as np
from typing import List, Dict, Any, Optional
import hashlib
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import logging


class FederatedLearning:
    """Federated Learning implementation for secure model aggregation
    with Azure ML integration."""

    def __init__(self, azure_ml_workspace: Optional[str] = None):
        """Initialize Federated Learning model with optional Azure ML
        integration."""
        self.model_parameters = None
        self.azure_ml_workspace = azure_ml_workspace
        self.logger = logging.getLogger(__name__)

        # Initialize Azure ML integration if workspace is provided
        if azure_ml_workspace:
            self._init_azure_ml_integration()

    def _init_azure_ml_integration(self):
        """Initialize Azure Machine Learning integration."""
        try:
            from azureml.core import Workspace, Experiment
            self.workspace = Workspace.get(name=self.azure_ml_workspace)
            self.experiment = Experiment(workspace=self.workspace,
                                         name='federated-learning')
            self.logger.info(
                f"Azure ML integration initialized for workspace: "
                f"{self.azure_ml_workspace}"
            )
        except ImportError:
            self.logger.warning(
                "Azure ML SDK not available. Running in local mode."
            )
        except Exception as e:
            self.logger.error(
                f"Failed to initialize Azure ML integration: {e}"
            )

    def federated_averaging(
        self, updates: List[Dict[str, Any]],
        weights: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Implement federated averaging algorithm with optional weighted
        averaging."""
        if not updates:
            raise ValueError("No updates provided for aggregation")

        if weights and len(weights) != len(updates):
            raise ValueError("Number of weights must match number of updates")

        aggregated_parameters = {}

        for key in updates[0].keys():
            if weights:
                # Weighted averaging
                weighted_sum = np.zeros_like(updates[0][key])
                total_weight = 0.0

                for i, update in enumerate(updates):
                    weight = weights[i]
                    weighted_sum += update[key] * weight
                    total_weight += weight

                aggregated_parameters[key] = weighted_sum / total_weight
            else:
                # Simple averaging
                param_list = [update[key] for update in updates]
                aggregated_parameters[key] = np.mean(param_list, axis=0)

        self.model_parameters = aggregated_parameters
        return aggregated_parameters

    def secure_aggregation(
        self, updates: List[Dict[str, Any]],
        secret_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Implement secure aggregation with differential privacy and
        encryption."""
        if secret_key:
            # Encrypt updates before aggregation
            encrypted_updates = []
            for update in updates:
                encrypted_updates.append(
                    self._encrypt_update(update, secret_key)
                )

            # For encrypted updates, we need to handle them differently
            # since they are dictionaries, not numpy arrays
            aggregated_encrypted = {}

            # Derive encryption key for HMAC calculation
            kdf = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'model-encryption',
                backend=default_backend()
            )
            derived_key = kdf.derive(secret_key.encode())

            # Aggregate each parameter separately
            for key in encrypted_updates[0].keys():
                if isinstance(encrypted_updates[0][key], dict):
                    # For encrypted parameters, we need to average the data
                    data_list = [
                        update[key]['data'] for update in encrypted_updates
                    ]
                    # Convert bytes back to numpy arrays for averaging
                    arrays = []
                    for i, data in enumerate(data_list):
                        shape = encrypted_updates[i][key]['shape']
                        dtype = encrypted_updates[i][key]['dtype']
                        array = np.frombuffer(data, dtype=np.dtype(dtype))
                        array = array.reshape(shape)
                        arrays.append(array)

                    # Average the arrays
                    avg_array = np.mean(arrays, axis=0)
                    # Compute new HMAC for the aggregated result
                    avg_bytes = avg_array.tobytes()
                    new_hmac = hmac.new(
                        derived_key, avg_bytes, hashlib.sha256
                    ).digest()
                    aggregated_encrypted[key] = {
                        'data': avg_bytes,
                        'hmac': new_hmac,
                        'shape': avg_array.shape,
                        'dtype': str(avg_array.dtype)
                    }
                else:
                    # For non-encrypted parameters, use standard averaging
                    param_list = [update[key] for update in encrypted_updates]
                    aggregated_encrypted[key] = np.mean(param_list, axis=0)

            # Decrypt the aggregated result
            decrypted_result = self._decrypt_update(
                aggregated_encrypted, secret_key
            )
            self.model_parameters = decrypted_result
            return decrypted_result
        else:
            # Fallback to standard federated averaging
            return self.federated_averaging(updates)

    def _encrypt_update(
        self, update: Dict[str, Any], secret_key: str
    ) -> Dict[str, Any]:
        """Encrypt model update using HMAC-based key derivation."""
        encrypted_update = {}

        # Derive encryption key from secret
        kdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'model-encryption',
            backend=default_backend()
        )
        derived_key = kdf.derive(secret_key.encode())

        for key, value in update.items():
            # Convert numpy arrays to bytes for encryption
            if isinstance(value, np.ndarray):
                value_bytes = value.tobytes()
                # Create HMAC for integrity verification
                hmac_digest = hmac.new(
                    derived_key, value_bytes, hashlib.sha256
                ).digest()
                encrypted_update[key] = {
                    'data': value_bytes,
                    'hmac': hmac_digest,
                    'shape': value.shape,
                    'dtype': str(value.dtype)
                }
            else:
                encrypted_update[key] = value

        return encrypted_update

    def _decrypt_update(
        self, encrypted_update: Dict[str, Any], secret_key: str
    ) -> Dict[str, Any]:
        """Decrypt model update and verify integrity."""
        decrypted_update = {}

        # Derive the same encryption key
        kdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'model-encryption',
            backend=default_backend()
        )
        derived_key = kdf.derive(secret_key.encode())

        for key, value in encrypted_update.items():
            if isinstance(value, dict) and 'data' in value:
                # Verify HMAC integrity
                expected_hmac = hmac.new(
                    derived_key, value['data'], hashlib.sha256
                ).digest()
                if value['hmac'] != expected_hmac:
                    raise ValueError(
                        f"HMAC verification failed for parameter {key}"
                    )

                # Reconstruct numpy array
                array = np.frombuffer(
                    value['data'], dtype=np.dtype(value['dtype'])
                )
                array = array.reshape(value['shape'])
                decrypted_update[key] = array
            else:
                decrypted_update[key] = value

        return decrypted_update

    def azure_ml_log_metrics(self, metrics: Dict[str, float]):
        """Log metrics to Azure ML workspace if configured."""
        if self.azure_ml_workspace:
            try:
                from azureml.core import Run
                run = Run.get_context()
                for name, value in metrics.items():
                    run.log(name, value)
                self.logger.info(f"Metrics logged to Azure ML: {metrics}")
            except ImportError:
                self.logger.warning(
                    "Azure ML SDK not available. Logging metrics locally."
                )
                self.logger.info(f"Local metrics: {metrics}")
            except Exception as e:
                self.logger.error(f"Failed to log metrics to Azure ML: {e}")
                self.logger.info(f"Local metrics: {metrics}")
        else:
            self.logger.info(f"Local metrics: {metrics}")

    def get_model_parameters(self) -> Dict[str, Any]:
        """Return the current model parameters."""
        return self.model_parameters

    def update_model(self, new_parameters: Dict[str, Any]):
        """Update the model with new parameters."""
        self.model_parameters = new_parameters

    def aggregate_updates(
        self, updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate model updates from multiple clients (backward
        compatibility)."""
        return self.federated_averaging(updates)
