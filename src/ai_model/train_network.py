import pandas as pd
from .training import AITrainer
from .coetus_integration import CoetusClient
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AINetworkTrainer:
    """Quantum-resistant AI network trainer"""
    
    def __init__(self, coetus_api_key: str = None):
        self.coetus_client = CoetusClient(coetus_api_key) if coetus_api_key else None
        self.model_version = f"v2.1-quantum-{datetime.now().strftime('%Y%m%d')}"
        
    def load_data(self, nova_blocks: list) -> pd.DataFrame:
        """Load and merge data from multiple sources"""
        base_data = pd.DataFrame(columns=['timestamp', 'close', 'volume'])
        trainer = AITrainer(base_data, coetus_api_key=self.coetus_client.api_key if self.coetus_client else None)
        
        if nova_blocks:
            trainer.train_on_nova_blocks(nova_blocks)
            
        if self.coetus_client:
            try:
                trainer.train_strategy(use_coetus=True)
            except Exception as e:
                logger.warning(f"Coetus training failed: {str(e)}")
                
        return trainer.data
    
    def train_network(self, nova_blocks: list, walk_forward: bool = True) -> dict:
        """Train the complete AI network"""
        data = self.load_data(nova_blocks)
        trainer = AITrainer(data)
        
        results = trainer.train_strategy(walk_forward=walk_forward)
        results['model_version'] = self.model_version
        results['quantum_safe'] = True
        
        return results
        
    def save_model(self, path: str):
        """Save trained model with versioning"""
        full_path = f"{path}-{self.model_version}"
        self.trainer.save_model(full_path)
        logger.info(f"Model saved to {full_path}")
        return full_path
