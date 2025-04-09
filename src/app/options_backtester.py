"""Backtesting module for options strategies"""
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
from .covered_call_strategy import CoveredCallStrategy

class OptionsBacktester:
    def __init__(self, strategy: CoveredCallStrategy):
        self.strategy = strategy
        self.results = {}
        
    def run_backtest(self, 
                   stock_data: pd.DataFrame,
                   options_data: pd.DataFrame,
                   initial_capital: float = 10000) -> Dict:
        """
        Backtest covered call strategy
        Args:
            stock_data: Historical stock prices
            options_data: Historical options chain data
            initial_capital: Starting capital
        """
        portfolio = pd.DataFrame(index=stock_data.index, columns=[
            'stock_value', 'premium_income', 'total_value', 
            'positions', 'returns', 'drawdown'
        ])
        
        # Initialize portfolio
        portfolio.iloc[0] = {
            'stock_value': initial_capital,
            'premium_income': 0,
            'total_value': initial_capital,
            'positions': {},
            'returns': 0,
            'drawdown': 0
        }
        
        for i in range(1, len(stock_data)):
            current_date = stock_data.index[i]
            current_price = stock_data.iloc[i]['close']
            
            # Get current options chain
            current_options = options_data[options_data['date'] == current_date]
            
            # Generate trades
            trade = self.strategy.select_optimal_call(
                stock_data.iloc[i]['ticker'], 
                current_price,
                current_options
            )
            
            # Update portfolio
            if trade:
                premium = trade['premium'] * 100  # Per contract
                portfolio.at[current_date, 'premium_income'] = premium
                portfolio.at[current_date, 'positions'] = {
                    'strike': trade['strike'],
                    'expiration': trade['expiration']
                }
            
            # Calculate portfolio metrics
            self._update_portfolio(portfolio, stock_data, i)
        
        self._calculate_performance(portfolio)
        return self.results
    
    def _update_portfolio(self, portfolio: pd.DataFrame,
                        stock_data: pd.DataFrame,
                        i: int) -> None:
        """Update portfolio metrics for current period"""
        prev = portfolio.iloc[i-1]
        current = stock_data.iloc[i]
        
        # Stock value change
        price_change = (current['close'] - stock_data.iloc[i-1]['close']) / stock_data.iloc[i-1]['close']
        stock_value = prev['stock_value'] * (1 + price_change)
        
        # Total portfolio value
        total_value = stock_value + portfolio.iloc[i]['premium_income']
        
        portfolio.at[stock_data.index[i], 'stock_value'] = stock_value
        portfolio.at[stock_data.index[i], 'total_value'] = total_value
        portfolio.at[stock_data.index[i], 'returns'] = (total_value - prev['total_value']) / prev['total_value']
        
        # Calculate drawdown
        peak = portfolio['total_value'].iloc[:i].max()
        portfolio.at[stock_data.index[i], 'drawdown'] = (total_value - peak) / peak
    
    def _calculate_performance(self, portfolio: pd.DataFrame) -> None:
        """Calculate comprehensive performance metrics"""
        returns = portfolio['returns']
        self.results = {
            'total_return': portfolio['total_value'].iloc[-1] / portfolio['total_value'].iloc[0] - 1,
            'annualized_return': np.mean(returns) * 252,
            'sharpe_ratio': np.mean(returns) / np.std(returns) * np.sqrt(252),
            'max_drawdown': portfolio['drawdown'].min(),
            'premium_yield': portfolio['premium_income'].sum() / portfolio['stock_value'].mean(),
            'win_rate': len(returns[returns > 0]) / len(returns)
        }
