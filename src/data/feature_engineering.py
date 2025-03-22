import pandas as pd

class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    def add_technical_indicators(self):
        """Add technical indicators to the dataset."""
        # Example: Calculate moving averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        # Additional indicators can be added here
        return self.data

    def add_volatility_indicators(self):
        """Add volatility indicators to the dataset."""
        self.data['Volatility'] = self.data['Close'].rolling(window=20).std()
        return self.data
