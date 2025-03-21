import pandas as pd

class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def preprocess(self):
        # Example preprocessing steps
        self.data.fillna(method='ffill', inplace=True)  # Fill missing values
        self.data.drop_duplicates(inplace=True)  # Remove duplicates
        # Convert date columns to numeric timestamps
        for column in self.data.select_dtypes(include=['object']).columns:
            try:
                self.data[column] = pd.to_datetime(self.data[column]).astype('int64') // 10**9  # Convert to seconds
            except (ValueError, TypeError):
                pass  # Ignore columns that cannot be converted
        # Convert date columns to timestamps
        for column in self.data.select_dtypes(include=['object']).columns:
            try:
                self.data[column] = pd.to_datetime(self.data[column]).astype(int) / 10**9  # Convert to seconds
            except (ValueError, TypeError):
                pass  # Ignore columns that cannot be converted
    def print_data_types(self):
        print(self.data.dtypes)

        return self.data
