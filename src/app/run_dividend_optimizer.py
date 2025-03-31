from src.data.data_loader import DataLoader
from dividend_optimizer import DividendOptimizer

# Load historical market data
data_loader = DataLoader('path/to/your/dividend_data.csv')  # Update with the actual path to your CSV file
data = data_loader.load_data()

if data is not None:
    # Create an instance of the DividendOptimizer
    dividend_optimizer = DividendOptimizer(data)

    # Optimize dividends
    optimized_stocks = dividend_optimizer.optimize_dividends()

    # Print the optimized stocks
    print("Optimized Dividend Stocks:")
    print(optimized_stocks)
else:
    print("Failed to load data.")
