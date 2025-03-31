import pandas as pd
import logging
from .trading_strategy import TradingStrategy  # Import the updated TradingStrategy class

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def run_backtest(self, data):
        """Run the backtest on the provided data."""
        initial_capital = 10000  # Starting capital
        positions = pd.DataFrame(index=data.index).fillna(0.0)
        portfolio = pd.Series(index=data.index).fillna(0.0)
        portfolio[0] = initial_capital  # Set initial capital

        # Implement the backtesting logic based on the strategy
        for date, row in data.iterrows():
            try:
                action = self.strategy.execute_trade(data.loc[:date])  # Get action from strategy
                # Update positions and portfolio based on action
                if "buy" in action:
                    positions[date] = 1  # Example: Buy one unit
                elif "sell" in action:
                    positions[date] = -1  # Example: Sell one unit

                # Update portfolio value
                portfolio[date] = portfolio[date - 1] + (positions[date] * row['close'])  # Update based on closing price
            except Exception as e:
                logger.error(f"Error during backtesting on {date}: {e}")

        return portfolio
