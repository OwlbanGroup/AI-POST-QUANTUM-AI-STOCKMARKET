from src.data.data_loader import DataLoader
from src.app.dividend_optimizer_enhanced import DividendOptimizer

# Load historical market data
data_loader = DataLoader('path/to/your/dividend_data.csv')  # Update with the actual path to your CSV file
data = data_loader.load_data()

# Initialize the DividendOptimizer with the loaded data
optimizer = DividendOptimizer(data)

# Optimize dividends and log the results
optimized_stocks = optimizer.optimize_dividends()
if optimized_stocks is not None:
    print("Optimized Stocks:")
    print(optimized_stocks)
else:
    print("No stocks were optimized.")
