import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DividendOptimizer:
    def __init__(self, data):
        self.data = data

    def calculate_dividend_yield(self):
        """Calculate the dividend yield for each stock."""
        try:
            self.data['dividend_yield'] = self.data['dividends'] / self.data['close']
            logger.info("Dividend yield calculated successfully.")
            return self.data
        except Exception as e:
            logger.error(f"Error calculating dividend yield: {e}")
            return None

    def filter_stocks(self, min_yield=0.03, max_payout_ratio=0.6):
        """Filter stocks based on dividend yield and payout ratio."""
        try:
            filtered_stocks = self.data[
                (self.data['dividend_yield'] >= min_yield) &
                (self.data['payout_ratio'] <= max_payout_ratio)
            ]
            logger.info("Stocks filtered successfully.")
            return filtered_stocks
        except Exception as e:
            logger.error(f"Error filtering stocks: {e}")
            return None

    def optimize_dividends(self):
        """Optimize the selection of dividend stocks."""
        self.calculate_dividend_yield()
        optimized_stocks = self.filter_stocks()
        if optimized_stocks is not None:
            logger.info("Dividend optimization completed successfully.")
        else:
            logger.warning("No stocks optimized.")
        return optimized_stocks
