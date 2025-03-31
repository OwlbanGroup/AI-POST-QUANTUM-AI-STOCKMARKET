import pandas as pd
# from data_loader import DataLoader
from trading_strategy import TradingStrategy
from backtesting import Backtester

# Load historical market data
data_loader = DataLoader('path/to/your/historical_data.csv')  # Update with the actual path to your CSV file
data = data_loader.load_data()

if data is not None:
    # Create an instance of the trading strategy
    trading_strategy = TradingStrategy()
    trading_strategy.set_strategy("momentum")  # Set the desired strategy

    # Create an instance of the backtester
    backtester = Backtester(trading_strategy)

    # Run the backtest
    results = backtester.run_backtest(data)

    # Print the results
    print("Backtest Results:")
    print(results)
else:
    print("Failed to load data.")
