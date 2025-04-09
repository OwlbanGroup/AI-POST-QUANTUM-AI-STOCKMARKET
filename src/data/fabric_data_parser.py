"""Enhanced Microsoft Fabric data parser with Azure integration"""
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.ai.ml import MLClient
import pandas as pd
import logging
from typing import Optional, Dict, Any

class FabricDataParser:
    def __init__(self, workspace_id: str, lakehouse_id: str,
                 storage_account: str = None, ml_workspace: str = None):
        """
        Initialize Fabric data parser
        Args:
            workspace_id: Fabric workspace ID
            lakehouse_id: Fabric lakehouse ID
        """
        self.credential = DefaultAzureCredential()
        self.workspace_id = workspace_id
        self.lakehouse_id = lakehouse_id
        self.logger = logging.getLogger(__name__)
        
        # Initialize Azure services
        self.storage_client = None
        self.ml_client = None
        
        if storage_account:
            self.storage_client = DataLakeServiceClient(
                account_url=f"https://{storage_account}.dfs.core.windows.net",
                credential=self.credential
            )
            
        if ml_workspace:
            self.ml_client = MLClient(
                credential=self.credential,
                workspace_name=ml_workspace
            )
        def load_data(self, table_name: str) -> Optional[pd.DataFrame]:
        """
        Load data from Fabric lakehouse table
        Args:
            table_name: Name of the table to load
        Returns:
            DataFrame with the loaded data or None if failed
        """
        try:
            self.logger.info(f"Loading data from table {table_name}")
            spark = self.client.spark.connect(
                workspace_id=self.workspace_id,
                lakehouse_id=self.lakehouse_id
            )
            df = spark.sql(f"SELECT * FROM {table_name}").toPandas()
            return df
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            return None

    def parse_options_data(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Parse options data from Fabric table
        Args:
            table_name: Name of the options data table
        Returns:
            Dictionary with parsed options data or None if failed
        """
        df = self.load_data(table_name)
        if df is None:
            return None
            
        try:
            # Convert to standard options data format
            df['expiration'] = pd.to_datetime(df['expiration'])
            df['quote_date'] = pd.to_datetime(df['quote_date'])
            
            return {
                'options_chain': df,
                'underlying_price': df['underlying_price'].iloc[0],
                'timestamp': df['quote_date'].max()
            }
        except Exception as e:
            self.logger.error(f"Error parsing options data: {str(e)}")
            return None

    def get_workspace_info(self) -> Dict[str, Any]:
        """Get information about the Fabric workspace"""
        try:
            return self.client.get_workspace(self.workspace_id)
        except Exception as e:
            self.logger.error(f"Error getting workspace info: {str(e)}")
            return {}
