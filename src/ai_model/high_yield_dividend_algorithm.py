import pandas as pd

# Load historical data
data = pd.read_csv('src/data/sample_data.csv')

# Calculate average closing price
average_close = data['close'].mean()

# Identify stocks with consistent upward trend
data['trend'] = data['close'].diff() > 0
consistent_upward_trend = data['trend'].all()

# Evaluate dividend yield (for demonstration, using a simple condition)
dividend_yield_threshold = 0.03  # Adjusted threshold for high-yield stocks
data['dividend_yield'] = (data['close'] - data['open']) / data['open']

# Identify high-yield dividend stocks
high_yield_stocks = data[data['dividend_yield'] > dividend_yield_threshold]

# Summary report with additional insights
summary_report = {
    'average_close': average_close,
    'consistent_upward_trend': consistent_upward_trend,
    'high_yield_stocks': high_yield_stocks,
    'total_high_yield_stocks': high_yield_stocks.shape[0],  # Count of high-yield stocks
    'high_yield_stocks_list': high_yield_stocks[['stock_name', 'dividend_yield']].to_dict(orient='records')  # List of high-yield stocks
}

print(summary_report)
