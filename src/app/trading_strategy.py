class TradingStrategy:
    def __init__(self):
        self.strategy = "default"

    def set_strategy(self, strategy):
        self.strategy = strategy
        return f"Trading strategy set to {strategy}."

    def execute_trade(self, market_analysis):
        # Implement trade execution logic based on market analysis
        if self.strategy == "high_yield":
            # Logic for high-yield strategy
            return "Executed trade based on high-yield strategy."
        elif self.strategy == "momentum":
            # Logic for momentum strategy
            return "Executed trade based on momentum strategy."
        else:
            return "Executed trade based on default strategy."
