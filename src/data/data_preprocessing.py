import pandas as pd

class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def preprocess(self):
        # Example preprocessing steps
        self.data.fillna(method='ffill', inplace=True)  # Fill missing values
        self.data.drop_duplicates(inplace=True)  # Remove duplicates
        return self.data
