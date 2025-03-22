import pandas as pd
import yfinance as yf

class RealTimeData:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_real_time_data(self):
        """Fetch real-time data for the specified ticker."""
        data = yf.download(self.ticker, period='1d', interval='1m')
        return data

    def process_data(self, data):
        """Process the real-time data for analysis."""
        # Example processing steps
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        # Additional processing can be added here
        return data
