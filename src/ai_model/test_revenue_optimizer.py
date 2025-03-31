import pandas as pd
from revenue_optimizer import RevenueOptimizer

# Sample data for testing
sample_data = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [5, 4, 3, 2, 1],
    'revenue': [100, 200, 300, 400, 500]  # Example revenue data
})

def test_revenue_optimizer():
    optimizer = RevenueOptimizer(sample_data)
    result = optimizer.optimize_revenue()
    print("Optimization Result:", result)

if __name__ == "__main__":
    test_revenue_optimizer()
