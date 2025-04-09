"""Track options positions and calculate P/L"""
import pandas as pd
from datetime import datetime
from typing import Dict, List

class PositionTracker:
    def __init__(self):
        self.positions = pd.DataFrame(columns=[
            'ticker', 'type', 'strike', 'expiration', 
            'premium', 'quantity', 'open_date', 'close_date',
            'close_price', 'status'
        ])
        self.closed_positions = pd.DataFrame(columns=self.positions.columns)

    def add_position(self, ticker: str, option_type: str, strike: float,
                   expiration: str, premium: float, quantity: int) -> None:
        """Add new options position"""
        new_position = {
            'ticker': ticker,
            'type': option_type,
            'strike': strike,
            'expiration': expiration,
            'premium': premium,
            'quantity': quantity,
            'open_date': datetime.now().strftime('%Y-%m-%d'),
            'close_date': None,
            'close_price': None,
            'status': 'open'
        }
        self.positions = self.positions.append(new_position, ignore_index=True)

    def close_position(self, ticker: str, strike: float, expiration: str,
                     close_price: float) -> None:
        """Close an existing position"""
        mask = (
            (self.positions['ticker'] == ticker) &
            (self.positions['strike'] == strike) &
            (self.positions['expiration'] == expiration) &
            (self.positions['status'] == 'open')
        )
        if mask.any():
            self.positions.loc[mask, 'status'] = 'closed'
            self.positions.loc[mask, 'close_date'] = datetime.now().strftime('%Y-%m-%d')
            self.positions.loc[mask, 'close_price'] = close_price
            
            # Move to closed positions
            closed = self.positions[mask]
            self.closed_positions = self.closed_positions.append(closed)
            self.positions = self.positions[~mask]

    def calculate_pnl(self) -> Dict[str, float]:
        """Calculate profit/loss for all positions"""
        open_pnl = (self.positions['premium'] * self.positions['quantity'] * 100).sum()
        
        closed_pnl = (
            (self.closed_positions['premium'] - 
             self.closed_positions['close_price']) * 
            self.closed_positions['quantity'] * 100
        ).sum()
        
        return {
            'open_positions_pnl': open_pnl,
            'closed_positions_pnl': closed_pnl,
            'total_pnl': open_pnl + closed_pnl
        }

    def get_expiring_positions(self, days: int = 7) -> pd.DataFrame:
        """Get positions expiring within X days"""
        today = datetime.now()
        return self.positions[
            (pd.to_datetime(self.positions['expiration']) - today).dt.days <= days
        ]
