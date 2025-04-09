"""Enhanced Microsoft Fabric data parser with Azure integration"""
import pandas as pd
import logging
from typing import Optional, Dict, Any

# Make Azure dependencies optional
AZURE_DEPS_AVAILABLE = False
DEPENDENCY_WARNINGS = []

try:
    from azure.identity import DefaultAzureCredential
    from azure.storage.filedatalake import DataLakeServiceClient
    AZURE_DEPS_AVAILABLE = True
except ImportError as e:
    class DefaultAzureCredential:
        def __init__(self):
            DEPENDENCY_WARNINGS.append("azure-identity not installed")
    class DataLakeServiceClient:
        def __init__(self): pass
    DEPENDENCY_WARNINGS.append(f"Azure Storage dependencies not available: {str(e)}")
            from azure.ai.ml import MLClient
except ImportError as e:
    class MLClient:
        def __init__(self): 
            DEPENDENCY_WARNINGS.append("azure-ai-ml not installed")
    DEPENDENCY_WARNINGS.append(f"Azure ML dependencies not available: {str(e)}")

try:
    from azure.synapse.spark import SparkClient
except ImportError as e:
    class SparkClient:
        def __init__(self): 
            DEPENDENCY_WARNINGS.append("azure-synapse-spark not installed")
    DEPENDENCY_WARNINGS.append(f"Azure Synapse dependencies not available: {str(e)}")

try:
    from delta.tables import DeltaTable
except ImportError as e:
    class DeltaTable:
        def __init__(self): 
            DEPENDENCY_WARNINGS.append("delta-spark not installed")
    DEPENDENCY_WARNINGS.append(f"Delta Lake dependencies not available: {str(e)}")
        def __init__(self, workspace_id: str, lakehouse_id: str,
                 storage_account: str = None, ml_workspace: str = None,
                 synapse_workspace: str = None):
        """
        Initialize Fabric data parser with OneLake support
        Args:
            workspace_id: Fabric workspace ID
            lakehouse_id: Fabric lakehouse ID
            storage_account: Azure Storage account name
            ml_workspace: Azure ML workspace name
            synapse_workspace: Azure Synapse workspace name
        """
        self.credential = DefaultAzureCredential()
        self.workspace_id = workspace_id
        self.lakehouse_id = lakehouse_id
        self.logger = logging.getLogger(__name__)
        
        # Initialize Azure services
        self.storage_client = None
        self.ml_client = None
        self.synapse_client = None
        
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
            
        if synapse_workspace:
            self.synapse_client = SparkClient(
                credential=self.credential,
                endpoint=f"https://{synapse_workspace}.dev.azuresynapse.net"
            )

    def load_data(self, table_name: str, delta_format: bool = False) -> Optional[pd.DataFrame]:
        """
        Load data from Fabric lakehouse table with OneLake support
        Args:
            table_name: Name of the table to load
            delta_format: Whether to load as Delta table
        Returns:
            DataFrame with the loaded data or None if failed
        """
        if not AZURE_DEPS_AVAILABLE:
            self.logger.warning("Azure dependencies not available - install required packages")
            return None
            
        try:
            self.logger.info(f"Loading data from table {table_name}")
            
            # Initialize Spark session
            spark = self.client.spark.connect(
                workspace_id=self.workspace_id,
                lakehouse_id=self.lakehouse_id
            )

            if delta_format:
                # Load as Delta table
                delta_path = f"abfss://{self.lakehouse_id}@onelake.dfs.fabric.microsoft.com/{self.workspace_id}/Tables/{table_name}"
                delta_table = DeltaTable.forPath(spark, delta_path)
                return delta_table.toDF().toPandas()
            else:
                # Standard load
                df = spark.sql(f"SELECT * FROM {table_name}").toPandas()
                return df
                
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}", exc_info=True)
            return None

    def parse_options_data(self, table_name: str, delta_format: bool = False) -> Optional[Dict[str, Any]]:
        """
        Parse options data from Fabric table with OneLake support
        Args:
            table_name: Name of the options data table
            delta_format: Whether to load as Delta table
        Returns:
            Dictionary with parsed options data or None if failed
        """
        df = self.load_data(table_name, delta_format=delta_format)
        if df is None:
            self.logger.warning(f"Failed to load options data from {table_name}")
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
            self.logger.error(f"Error parsing options data: {str(e)}", exc_info=True)
            return None

    def get_workspace_info(self) -> Dict[str, Any]:
        """Get information about the Fabric workspace"""
        try:
            info = self.client.get_workspace(self.workspace_id)
            if self.synapse_client:
                info['synapse_pools'] = self.synapse_client.list_spark_pools()
            return info
        except Exception as e:
            self.logger.error(f"Error getting workspace info: {str(e)}", exc_info=True)
            return {}
            
    def export_to_powerbi(self, df: pd.DataFrame, dataset_name: str) -> bool:
        """
        Export DataFrame to Power BI dataset
        Args:
            df: DataFrame to export
            dataset_name: Name of Power BI dataset
        Returns:
            True if successful, False otherwise
        """
        try:
            from powerbiclient import Report, models
            report = Report(group_id=self.workspace_id)
            dataset = models.Dataset(name=dataset_name)
            report.add_dataset(dataset, df)
            return True
        except ImportError:
            self.logger.warning("Power BI client not available - install with 'pip install powerbiclient'")
            return False
        except Exception as e:
            self.logger.error(f"Error exporting to Power BI: {str(e)}", exc_info=True)
            return False
