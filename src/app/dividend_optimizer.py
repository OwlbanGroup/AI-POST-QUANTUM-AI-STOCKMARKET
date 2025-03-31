import pandas as pd

class DividendOptimizer:
    def __init__(self, data):
        self.data = data

    def calculate_dividend_yield(self):
        """Calculate the dividend yield for each stock."""
        self.data['dividend_yield'] = self.data['dividends'] / self.data['close']
        return self.data

    def filter_stocks(self, min_yield=0.03, max_payout_ratio=0.6):
        """Filter stocks based on dividend yield and payout ratio."""
        filtered_stocks = self.data[
            (self.data['dividend_yield'] >= min_yield) &
            (self.data['payout_ratio'] <= max_payout_ratio)
        ]
        return filtered_stocks

    def optimize_dividends(self):
        """Optimize the selection of dividend stocks."""
        self.calculate_dividend_yield()
        optimized_stocks = self.filter_stocks()
        return optimized_stocks
