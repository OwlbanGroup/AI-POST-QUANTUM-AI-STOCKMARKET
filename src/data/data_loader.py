import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        # Load data from a CSV file
        try:
            try:
        data = pd.read_csv(self.file_path)





































































        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            return None
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            return None
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return None
        except pd.errors.ParserError:
            print("Error: The file could not be parsed. Please check the file format.")
            return None
        return data
