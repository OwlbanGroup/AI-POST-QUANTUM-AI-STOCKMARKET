"""AI Covered Call Options Trading Strategy"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from datetime import datetime, timedelta
try:
    import yfinance as yf
except ImportError:
    raise ImportError(
        "yfinance package required but not found. "
        "Install with: pip install yfinance>=0.1.70"
    )

class CoveredCallStrategy:
    def __init__(self, underlying_holdings: Dict):
        """
        Initialize with current stock holdings
        Args:
            underlying_holdings: Dict of {ticker: shares_owned}
        """
        self.holdings = underlying_holdings
        self.option_chain = None
        from .position_tracker import PositionTracker
        self.position_tracker = PositionTracker()
        self.iv_percentile_threshold = 0.7  # Only sell calls when IV > 70th percentile
        self.min_dte = 14  # Minimum days to expiration
        self.max_dte = 45  # Maximum days to expiration
        self.delta_target = 0.3  # Target call option delta
        self.min_premium = 0.02  # Minimum premium as % of stock price

    def fetch_option_chain(self, ticker: str) -> pd.DataFrame:
        """Retrieve live option chain data from yfinance"""
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            if not expirations:
                return pd.DataFrame()
                
            # Get nearest expiration within our target range
            valid_expirations = [
                exp for exp in expirations 
                if self.min_dte <= (datetime.strptime(exp, '%Y-%m-%d') - datetime.now()).days <= self.max_dte
            ]
            if not valid_expirations:
                return pd.DataFrame()
                
            chain = stock.option_chain(valid_expirations[0]).calls
            return chain[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'openInterest']].rename(columns={
                'lastPrice': 'last',
                'impliedVolatility': 'iv',
                'openInterest': 'oi'
            })
        except Exception as e:
            print(f"Error fetching options chain: {e}")
            return pd.DataFrame()
    def select_optimal_call(self, ticker: str, current_price: float) -> Dict:
        """
        Select the best call option to sell based on:
        - IV percentile
        - Delta target
        - Days to expiration
        - Premium amount
        """
        chain = self.fetch_option_chain(ticker)
        qualified = chain[
            (chain['iv_percentile'] >= self.iv_percentile_threshold) &
            (chain['delta'].between(self.delta_target-0.05, self.delta_target+0.05)) &
            (chain['expiration'] <= datetime.now() + timedelta(days=self.max_dte)) &
            (chain['expiration'] >= datetime.now() + timedelta(days=self.min_dte)) &
            ((chain['bid']/current_price) >= self.min_premium)
        ]
        
        if not qualified.empty:
            optimal = qualified.nlargest(1, 'bid').iloc[0]
            return {
                'ticker': ticker,
                'action': 'SELL_CALL',
                'strike': optimal['strike'],
                'expiration': optimal['expiration'],
                'premium': optimal['bid'],
                'delta': optimal['delta'],
                'iv_percentile': optimal['iv_percentile']
            }
        return None

    def generate_trades(self, portfolio: Dict, market_data: pd.DataFrame) -> Dict:
        """
        Generate covered call trades for entire portfolio
        Args:
            portfolio: Dict of {ticker: {'shares': int, 'cost_basis': float}}
            market_data: DataFrame with current prices
        Returns:
            Dict of recommended trades
        """
        trades = {}
        for ticker, position in portfolio.items():
            if position['shares'] >= 100:  # Standard option contract size
                current_price = market_data.loc[ticker]['close']
                trade = self.select_optimal_call(ticker, current_price)
                if trade:
                    trades[ticker] = trade
                    # Track the new position
                    self.position_tracker.add_position(
                    ticker=ticker,
                    option_type='CALL',
                    strike=trade['strike'],
                    expiration=trade['expiration'],
                    premium=trade['premium'],
                    quantity=position['shares'] // 100
                )
        return trades
    def calculate_metrics(self, trades: Dict) -> Dict:
        """Calculate strategy performance metrics"""
        total_premium = sum(trade['premium']*100 for trade in trades.values())
        capital_employed = sum(100*trade['strike'] for trade in trades.values())
        return {
            'estimated_annualized_return': (total_premium/capital_employed)*12,
            'downside_protection': total_premium,
            'breakeven_price': {t: trade['strike']+trade['premium'] for t, trade in trades.items()}
        }
