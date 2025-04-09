import pandas as pd
import numpy as np
import logging
from typing import Dict, List
from datetime import datetime
from .trading_strategy import TradingStrategy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, strategy: TradingStrategy, initial_capital: float = 10000):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.results = {}
        
    def run_backtest(self, data: pd.DataFrame, walk_forward: bool = False) -> Dict:
        """Run backtest with optional walk-forward validation."""
        if walk_forward:
            return self._run_walk_forward(data)
            
        portfolio = pd.DataFrame(index=data.index, columns=[
            'value', 'returns', 'cum_returns', 'drawdown', 'positions'
        ])
        portfolio.iloc[0] = {
            'value': self.initial_capital,
            'returns': 0,
            'cum_returns': 0,
            'drawdown': 0,
            'positions': 0
        }
        
        for i in range(1, len(data)):
            try:
                trade_data = data.iloc[:i]
                trade_result = self.strategy.execute_trade(trade_data)
                
                # Update positions and portfolio
                position_size = self._calculate_position_size(trade_result)
                portfolio.at[data.index[i], 'positions'] = position_size
                
                # Calculate portfolio metrics
                self._update_portfolio_metrics(portfolio, data, i, position_size)
                
            except Exception as e:
                logger.error(f"Backtest error at {data.index[i]}: {e}")
                
        self._calculate_performance_metrics(portfolio)
        return self.results
        
    def _run_walk_forward(self, data: pd.DataFrame, 
                         train_size: float = 0.7,
                         n_splits: int = 5) -> Dict:
        """Run walk-forward backtesting with multiple train/test periods.
        
        Args:
            data: Historical market data
            train_size: Percentage of data to use for training (0-1)
            n_splits: Number of walk-forward splits to perform
            
        Returns:
            Aggregated performance metrics across all test periods
        """
        total_days = len(data)
        train_days = int(total_days * train_size)
        test_days = total_days - train_days
        step_size = test_days // n_splits
        
        all_results = []
        
        for i in range(n_splits):
            # Split data into train/test periods
            train_start = i * step_size
            train_end = train_start + train_days
            test_end = min(train_end + test_days, total_days)
            
            train_data = data.iloc[train_start:train_end]
            test_data = data.iloc[train_end:test_end]
            
            # Train strategy on in-sample period
            if hasattr(self.strategy, 'train'):
                self.strategy.train(train_data)
            
            # Test on out-of-sample period
            test_results = self.run_backtest(test_data)
            all_results.append(test_results)
            
            logger.info(f"Walk-forward split {i+1}/{n_splits} complete")
            
        # Aggregate results across all test periods
        return {
            'average_return': np.mean([r['total_return'] for r in all_results]),
            'average_sharpe': np.mean([r['sharpe_ratio'] for r in all_results]),
            'max_drawdown': min([r['max_drawdown'] for r in all_results]),
            'win_rate': np.mean([r['win_rate'] for r in all_results]),
            'all_results': all_results
        }
    def _calculate_position_size(self, trade_result: Dict) -> float:
        """Calculate position size based on strategy parameters."""
        if 'size' in trade_result:
            return trade_result['size']
        return self.strategy.max_position_size * self.initial_capital
        
    def _update_portfolio_metrics(self, portfolio: pd.DataFrame, 
                                data: pd.DataFrame, i: int, 
                                position_size: float) -> None:
        """Update portfolio metrics for current time period."""
        prev_value = portfolio.iloc[i-1]['value']
        price_change = (data.iloc[i]['close'] - data.iloc[i-1]['close']) / data.iloc[i-1]['close']
        
        portfolio.at[data.index[i], 'value'] = prev_value + (position_size * price_change)
        portfolio.at[data.index[i], 'returns'] = (position_size * price_change) / prev_value
        portfolio.at[data.index[i], 'cum_returns'] = (portfolio.iloc[i]['value'] - self.initial_capital) / self.initial_capital
        portfolio.at[data.index[i], 'drawdown'] = (portfolio.iloc[i]['value'] - portfolio.iloc[:i]['value'].max()) / portfolio.iloc[:i]['value'].max()
        
    def _calculate_performance_metrics(self, portfolio: pd.DataFrame) -> None:
        """Calculate comprehensive performance metrics."""
        returns = portfolio['returns']
        self.results = {
            'total_return': portfolio.iloc[-1]['cum_returns'],
            'annualized_return': np.mean(returns) * 252,
            'annualized_volatility': np.std(returns) * np.sqrt(252),
            'sharpe_ratio': np.mean(returns) / np.std(returns) * np.sqrt(252),
            'max_drawdown': portfolio['drawdown'].min(),
            'win_rate': len(returns[returns > 0]) / len(returns),
            'profit_factor': returns[returns > 0].sum() / abs(returns[returns < 0].sum()),
            'portfolio': portfolio
        }
