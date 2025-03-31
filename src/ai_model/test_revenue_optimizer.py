import pandas as pd
from revenue_optimizer import RevenueOptimizer

# Sample data for testing
sample_data = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [5, 4, 3, 2, 1],
    'revenue': [100, 200, 300, 400, 500]  # Example revenue data
})

def run_tests():
    for _ in range(3):
        test_revenue_optimizer()
    for _ in range(6):
        test_revenue_optimizer()
    for _ in range(9):
        test_revenue_optimizer()
    for _ in range(7):
        test_revenue_optimizer()

if __name__ == "__main__":
    run_tests()

if __name__ == "__main__":
    test_revenue_optimizer()
