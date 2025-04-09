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

    # Check if options backtest is needed
    if hasattr(trading_strategy, 'options_strategy') and trading_strategy.options_strategy:
        from .options_backtester import OptionsBacktester
        options_data = DataLoader('src/data/sample_options_data.csv').load_data()
        options_backtester = OptionsBacktester(trading_strategy.options_handler)
        results = options_backtester.run_backtest(data, options_data)
        print("Options Backtest Results:")
    else:
        # Run regular backtest
        results = backtester.run_backtest(data)
        print("Backtest Results:")
    
    print(results)
else:
    print("Failed to load data.")
