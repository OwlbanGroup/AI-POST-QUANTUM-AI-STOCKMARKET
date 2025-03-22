import pandas as pd
import yfinance as yf

class DataHandler:
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_data(self, start_date, end_date):
        """Fetch historical stock data from Yahoo Finance."""
        data = {}
        for ticker in self.tickers:
            data[ticker] = yf.download(ticker, start=start_date, end=end_date)
        return data

    def preprocess_data(self, data):
        """Preprocess the fetched data."""
        # Example preprocessing steps
        for ticker in data:
            df = data[ticker]
            df.dropna(inplace=True)  # Remove missing values
            # Additional preprocessing steps can be added here
        return data
