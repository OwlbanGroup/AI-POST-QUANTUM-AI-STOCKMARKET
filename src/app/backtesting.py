import pandas as pd

class Backtester:
    def __init__(self, strategy):
        self.strategy = strategy

    def run_backtest(self, data):
        """Run the backtest on the provided data."""
        initial_capital = 10000  # Starting capital
        positions = pd.DataFrame(index=data.index).fillna(0.0)
        portfolio = pd.Series(index=data.index)

        # Implement the backtesting logic based on the strategy
        for date, row in data.iterrows():
            action = self.strategy.decide_action(row)  # Get action from strategy
            # Update positions and portfolio based on action
            # Example: Buy or sell logic can be implemented here

        return portfolio
