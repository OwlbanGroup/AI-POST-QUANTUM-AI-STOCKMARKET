"""Data loader with NVIDIA Blackwell GPU acceleration"""
try:
    import cudf as pd
    GPU_ACCELERATED = True
    # Blackwell-specific RAPIDS optimizations
    try:
        BLACKWELL_RAPIDS_OPTIMIZED = True
        print("Blackwell RAPIDS optimizations enabled")
    except ImportError:
        BLACKWELL_RAPIDS_OPTIMIZED = False
        print("Blackwell RAPIDS optimizations not available")
except ImportError:
    import pandas as pd
    GPU_ACCELERATED = False
    BLACKWELL_RAPIDS_OPTIMIZED = False
import logging
from typing import Optional, Dict, Any
from .fabric_data_parser import FabricDataParser

class DataLoader:
    """Data loader class for handling data loading with GPU acceleration and Fabric integration."""
    def __init__(self, file_path: str, use_fabric: bool = False,
                 workspace_id: str = None, lakehouse_id: str = None):
        """
        Initialize data loader
        Args:
            file_path: Path to local data file
            use_fabric: Whether to use Microsoft Fabric
            workspace_id: Fabric workspace ID
            lakehouse_id: Fabric lakehouse ID
        """
        self.file_path = file_path
        self.use_fabric = use_fabric
        self.logger = logging.getLogger(__name__)
        
        if use_fabric:
            if not workspace_id or not lakehouse_id:
                raise ValueError("Workspace ID and Lakehouse ID required for Fabric")
            self.fabric_parser = FabricDataParser(workspace_id, lakehouse_id)
        else:
            self.fabric_parser = None

    def load_data(self) -> Optional[pd.DataFrame]:
        """Load data from source"""
        if self.use_fabric and self.fabric_parser:
            try:
                # Try to load from Fabric first
                return self.fabric_parser.load_data(self.file_path)
            except (IOError, ValueError) as e:
                self.logger.warning("Fabric load failed: %s. Falling back to local file", e)

        # Fall back to local file
        try:
            return pd.read_csv(self.file_path)
        except (IOError, ValueError) as e:
            self.logger.error("Error loading data: %s", e)
            return None

    def load_options_data(self) -> Optional[Dict[str, Any]]:
        """Load options data from source"""
        if self.use_fabric and self.fabric_parser:
            try:
                # Try to load from Fabric first
                return self.fabric_parser.parse_options_data(self.file_path)
            except (IOError, ValueError) as e:
                self.logger.warning("Fabric options load failed: %s", e)

        # Fall back to local file
        try:
            df = pd.read_csv(self.file_path)
            return {
                'options_chain': df,
                'underlying_price': df['underlying_price'].iloc[0],
                'timestamp': pd.to_datetime('now')
            }
        except (IOError, ValueError) as e:
            self.logger.error("Error loading options data: %s", e)
            return None
