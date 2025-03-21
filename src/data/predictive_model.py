import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load historical stock data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Prepare data for training
def prepare_data(data):
    # Assuming 'date' is a column and we want to predict 'close' prices
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data = data[['close']]  # Select relevant features
    return data

# Train the predictive model
def train_model(data):
    X = data.index.values.astype(int).reshape(-1, 1)  # Convert date index to integer and reshape
    y = data['close'].values  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions, squared=False)  # Corrected line

    print(f'Model Evaluation: MAE = {mae}, RMSE = {rmse}')
    return model

# Main function to execute the predictive analytics
if __name__ == "__main__":
    file_path = 'src/data/sample_data.csv'
    data = load_data(file_path)
    prepared_data = prepare_data(data)
    model = train_model(prepared_data)
