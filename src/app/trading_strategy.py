import pandas as pd
import numpy as np
from typing import Dict, Tuple

class TradingStrategy:
    def __init__(self, predictive_model=None, max_position_size=0.1, stop_loss_pct=0.05):
    
        self.indicators = {}
        self.predictive_model = predictive_model
        self.max_position_size = max_position_size  # Max % of capital per trade
        self.stop_loss_pct = stop_loss_pct  # Stop loss percentage
        self.portfolio_value = 0
    def set_strategy(self, strategy: str) -> str:
        """Set the trading strategy to use."""
        self.strategy = strategy
        return f"Trading strategy set to {strategy}."

    def calculate_moving_average(self, data: pd.DataFrame, window: int) -> pd.Series:
        """Calculate simple moving average."""
        return data['close'].rolling(window=window).mean()

    def calculate_rsi(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI)."""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """Calculate MACD indicator."""
        ema_fast = data['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = data['close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return {'macd': macd, 'signal': signal_line, 'histogram': histogram}

    def calculate_bollinger_bands(self, data: pd.DataFrame, window: int = 20, num_std: float = 2) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands."""
        sma = data['close'].rolling(window=window).mean()
        rolling_std = data['close'].rolling(window=window).std()
        upper_band = sma + (rolling_std * num_std)
        lower_band = sma - (rolling_std * num_std)
        return {'upper': upper_band, 'middle': sma, 'lower': lower_band}

    def calculate_stochastic(self, data: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> Dict[str, pd.Series]:
        """Calculate Stochastic Oscillator."""
        low_min = data['low'].rolling(window=k_window).min()
        high_max = data['high'].rolling(window=k_window).max()
        k = 100 * ((data['close'] - low_min) / (high_max - low_min))
        d = k.rolling(window=d_window).mean()
        return {'k': k, 'd': d}

    def calculate_multi_timeframe(self, data: pd.DataFrame, primary_tf: str, secondary_tf: str) -> pd.DataFrame:
        """Calculate multi-timeframe indicators."""
        resampled = data.resample(secondary_tf).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        return resampled

    def update_indicators(self, data: pd.DataFrame) -> None:
        """Calculate and store all technical indicators."""
        self.indicators = {
            'ma_20': self.calculate_moving_average(data, 20),
            'ma_50': self.calculate_moving_average(data, 50),
            'rsi': self.calculate_rsi(data),
            'macd': self.calculate_macd(data),
            'bollinger': self.calculate_bollinger_bands(data),
            'stochastic': self.calculate_stochastic(data)
        }

    def execute_trade(self, market_analysis: pd.DataFrame) -> str:
        """Execute trades based on selected strategy and market conditions."""
        self.update_indicators(market_analysis)
        latest = market_analysis.iloc[-1]
        indicators = self.indicators
        
        if self.strategy == "high_yield":
            # Enhanced high-yield strategy using Bollinger Bands
            if latest['close'] < indicators['bollinger']['lower'].iloc[-1]:
                return "Executed buy trade based on high-yield strategy (oversold)."
            elif latest['close'] > indicators['bollinger']['upper'].iloc[-1]:
                return "Executed sell trade based on high-yield strategy (overbought)."
            return "No trade executed based on high-yield strategy."
            
        elif self.strategy == "momentum":
            # Enhanced momentum strategy using multiple indicators
            ma_cross = latest['close'] > indicators['ma_20'].iloc[-1]
            rsi_oversold = indicators['rsi'].iloc[-1] < 30
            stoch_oversold = (indicators['stochastic']['k'].iloc[-1] < 20 and 
                            indicators['stochastic']['d'].iloc[-1] < 20)
            macd_bullish = (indicators['macd']['macd'].iloc[-1] > 
                          indicators['macd']['signal'].iloc[-1])
            
            if ma_cross and (rsi_oversold or stoch_oversold) and macd_bullish:
                return "Executed buy trade based on enhanced momentum strategy."
                
            ma_cross = latest['close'] < indicators['ma_20'].iloc[-1]
            rsi_overbought = indicators['rsi'].iloc[-1] > 70
            stoch_overbought = (indicators['stochastic']['k'].iloc[-1] > 80 and 
                              indicators['stochastic']['d'].iloc[-1] > 80)
            macd_bearish = (indicators['macd']['macd'].iloc[-1] < 
                          indicators['macd']['signal'].iloc[-1])
            
            if ma_cross and (rsi_overbought or stoch_overbought) and macd_bearish:
                return "Executed sell trade based on enhanced momentum strategy."
                
            return "No trade executed based on momentum strategy."
            
        elif self.strategy == "multi_timeframe":
            # Multi-timeframe strategy example
            higher_tf = self.calculate_multi_timeframe(market_analysis, '1D', '1W')
            if higher_tf['close'].iloc[-1] > higher_tf['close'].iloc[-2]:
                return "Executed buy trade based on weekly uptrend."
            else:
                return "Executed sell trade based on weekly downtrend."
                
        else:
            return "Executed trade based on default strategy."
