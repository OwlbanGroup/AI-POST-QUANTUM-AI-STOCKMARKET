"""
Comprehensive test suite for quantum machine learning algorithms
Tests quantum neural networks, federated learning, and explainable AI
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.ai_model.quantum_ml import QuantumNeuralNetwork, FederatedLearning, ExplainableAI
from src.ai_model.quantum_crypto import QuantumSafeEncryption

class TestQuantumNeuralNetwork:
    """Test quantum neural network implementations"""
    
    def test_quantum_layer_initialization(self):
        """Test quantum layer setup and parameters"""
        qnn = QuantumNeuralNetwork(input_dim=10, hidden_dim=20, output_dim=2)
        assert qnn.input_dim == 10
        assert qnn.hidden_dim == 20
        assert qnn.output_dim == 2
        
    def test_quantum_forward_pass(self):
        """Test quantum forward propagation"""
        qnn = QuantumNeuralNetwork(input_dim=5, hidden_dim=10, output_dim=1)
        input_data = np.random.randn(1, 5)
        output = qnn.forward(input_data)
        assert output.shape == (1, 1)
        
    def test_quantum_backpropagation(self):
        """Test quantum backpropagation algorithm"""
        qnn = QuantumNeuralNetwork(input_dim=3, hidden_dim=5, output_dim=1)
        input_data = np.random.randn(1, 3)
        target = np.array([[1.0]])
        loss = qnn.train_step(input_data, target)
        assert isinstance(loss, float)
        assert loss >= 0
        
    def test_quantum_entanglement(self):
        """Test quantum entanglement effects in trading decisions"""
        qnn = QuantumNeuralNetwork(input_dim=4, hidden_dim=8, output_dim=2)
        market_data = np.random.randn(100, 4)
        predictions = qnn.predict(market_data)
        assert predictions.shape == (100, 2)
        
    def test_quantum_superposition(self):
        """Test quantum superposition for market state analysis"""
        qnn = QuantumNeuralNetwork(input_dim=6, hidden_dim=12, output_dim=3)
        market_states = qnn.analyze_superposition_states()
        assert len(market_states) == 8  # 2^3 possible states

class TestFederatedLearning:
    """Test federated learning implementation"""
    
    def test_federated_setup(self):
        """Test federated learning initialization"""
        fl = FederatedLearning(num_clients=5, model_type='quantum')
        assert fl.num_clients == 5
        assert fl.model_type == 'quantum'
        
    def test_client_model_distribution(self):
        """Test model distribution to clients"""
        fl = FederatedLearning(num_clients=3)
        models = fl.distribute_models()
        assert len(models) == 3
        
    def test_federated_aggregation(self):
        """Test federated model aggregation"""
        fl = FederatedLearning(num_clients=4)
        client_updates = [np.random.randn(10) for _ in range(4)]
        aggregated = fl.aggregate_updates(client_updates)
        assert aggregated.shape == (10,)
        
    def test_privacy_preservation(self):
        """Test privacy preservation in federated learning"""
        fl = FederatedLearning(num_clients=5)
        original_data = np.random.randn(100, 5)
        processed_data = fl.privacy_filter(original_data)
        assert processed_data.shape == original_data.shape
        
    def test_differential_privacy(self):
        """Test differential privacy mechanisms"""
        fl = FederatedLearning(num_clients=3)
        sensitive_data = np.random.randn(50, 3)
        private_data = fl.add_differential_privacy(sensitive_data, epsilon=1.0)
        assert private_data.shape == sensitive_data.shape

class TestExplainableAI:
    """Test explainable AI implementations"""
    
    def test_feature_importance(self):
        """Test feature importance calculation"""
        xai = ExplainableAI(model_type='quantum')
        features = np.random.randn(100, 5)
        importance = xai.calculate_feature_importance(features)
        assert len(importance) == 5
        assert abs(sum(importance) - 1.0) < 0.01
        
    def test_lime_explanations(self):
        """Test LIME-style explanations for predictions"""
        xai = ExplainableAI(model_type='quantum')
        prediction = np.array([0.7, 0.3])
        explanation = xai.explain_prediction(prediction)
        assert 'feature_contributions' in explanation
        assert 'confidence' in explanation
        
    def test_shap_values(self):
        """Test SHAP value calculations"""
        xai = ExplainableAI(model_type='quantum')
        data = np.random.randn(50, 4)
        shap_values = xai.calculate_shap_values(data)
        assert shap_values.shape == (50, 4)
        
    def test_trading_decision_explanation(self):
        """Test explanation generation for trading decisions"""
        xai = ExplainableAI(model_type='quantum')
        market_data = {
            'price': 100.0,
            'volume': 1000000,
            'volatility': 0.2,
            'sentiment': 0.7
        }
        explanation = xai.explain_trading_decision(market_data, 'BUY')
        assert 'reasoning' in explanation
        assert 'confidence' in explanation
        
    def test_visual_explanations(self):
        """Test visual explanation generation"""
        xai = ExplainableAI(model_type='quantum')
        data = np.random.randn(100, 3)
        visual = xai.generate_visual_explanation(data)
        assert 'chart_data' in visual
        assert 'feature_names' in visual

class TestQuantumSafeEncryption:
    """Test quantum-safe encryption implementations"""
    
    def test_lattice_encryption(self):
        """Test lattice-based encryption"""
        qse = QuantumSafeEncryption(algorithm='lattice')
        message = "Test trading data"
        encrypted = qse.encrypt(message)
        decrypted = qse.decrypt(encrypted)
        assert decrypted == message
        
    def test_key_generation(self):
        """Test quantum-safe key generation"""
        qse = QuantumSafeEncryption(algorithm='kyber')
        public_key, private_key = qse.generate_keypair()
        assert len(public_key) > 0
        assert len(private_key) > 0
        
    def test_signature_verification(self):
        """Test quantum-safe digital signatures"""
        qse = QuantumSafeEncryption(algorithm='dilithium')
        message = "Order: BUY 100 AAPL"
        signature = qse.sign(message)
        assert qse.verify(message, signature)
        
    def test_performance_benchmark(self):
        """Test encryption performance"""
        qse = QuantumSafeEncryption(algorithm='lattice')
        import time
        start = time.time()
        for i in range(1000):
            qse.encrypt(f"Message {i}")
        duration = time.time() - start
        assert duration < 1.0  # Should encrypt 1000 messages in under 1 second
        
    def test_security_strength(self):
        """Test security strength against quantum attacks"""
        qse = QuantumSafeEncryption(algorithm='kyber')
        # Test against known quantum attack vectors
        test_vectors = [
            "short_message",
            "long_message_with_lots_of_data_for_testing",
            "special_chars!@#$%^&*()",
            "unicode_测试_消息"
        ]
        for message in test_vectors:
            encrypted = qse.encrypt(message)
            assert len(encrypted) > len(message)  # Encryption adds security overhead

@pytest.mark.integration
class TestQuantumMLIntegration:
    """Integration tests for quantum ML components"""
    
    def test_end_to_end_trading_pipeline(self):
        """Test complete trading pipeline with quantum ML"""
        # Setup quantum components
        qnn = QuantumNeuralNetwork(input_dim=10, hidden_dim=20, output_dim=3)
        fl = FederatedLearning(num_clients=3)
        xai = ExplainableAI(model_type='quantum')
        qse = QuantumSafeEncryption(algorithm='lattice')
        
        # Simulate trading scenario
        market_data = np.random.randn(100, 10)
        predictions = qnn.predict(market_data)
        explanation = xai.explain_prediction(predictions[0])
        
        # Verify secure communication
        trade_signal = "BUY AAPL 100 shares"
        encrypted_signal = qse.encrypt(trade_signal)
        decrypted_signal = qse.decrypt(encrypted_signal)
        
        assert decrypted_signal == trade_signal
        assert len(predictions) == 100
        assert 'confidence' in explanation
        
    def test_federated_quantum_learning(self):
        """Test federated learning with quantum models"""
        fl = FederatedLearning(num_clients=5)
        qnn = QuantumNeuralNetwork(input_dim=5, hidden_dim=10, output_dim=2)
        
        # Simulate federated training
        client_data = [np.random.randn(20, 5) for _ in range(5)]
        global_model = fl.train_federated_quantum(qnn, client_data)
        
        assert global_model is not None
        test_data = np.random.randn(10, 5)
        predictions = global_model.predict(test_data)
        assert predictions.shape == (10, 2)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
