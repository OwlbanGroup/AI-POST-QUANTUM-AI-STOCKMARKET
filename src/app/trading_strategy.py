import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self):
        self.strategy = "default"

    def set_strategy(self, strategy):
        self.strategy = strategy
        return f"Trading strategy set to {strategy}."

    def calculate_moving_average(self, data, window):
        """Calculate the moving average."""
        return data['close'].rolling(window=window).mean()

    def calculate_rsi(self, data, window=14):
        """Calculate the Relative Strength Index (RSI)."""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def execute_trade(self, market_analysis):
        # Implement trade execution logic based on market analysis
        if self.strategy == "high_yield":
            # Logic for high-yield strategy
            return "Executed trade based on high-yield strategy."
        elif self.strategy == "momentum":
            # Logic for momentum strategy using moving average and RSI
            moving_average = self.calculate_moving_average(market_analysis, window=20)
            rsi = self.calculate_rsi(market_analysis)
            if market_analysis['close'].iloc[-1] > moving_average.iloc[-1] and rsi.iloc[-1] < 30:
                return "Executed buy trade based on momentum strategy."
            elif market_analysis['close'].iloc[-1] < moving_average.iloc[-1] and rsi.iloc[-1] > 70:
                return "Executed sell trade based on momentum strategy."
            else:
                return "No trade executed based on momentum strategy."
        else:
            return "Executed trade based on default strategy."
