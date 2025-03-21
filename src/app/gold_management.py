class GoldManagement:
    def __init__(self):
        self.gold_reserves = 0  # Total gold reserves in ounces

    def add_gold(self, amount):
        self.gold_reserves += amount
        return f"Added {amount} ounces of gold. Total reserves: {self.gold_reserves} ounces."

    def remove_gold(self, amount):
        if amount <= self.gold_reserves:
            self.gold_reserves -= amount
            return f"Removed {amount} ounces of gold. Total reserves: {self.gold_reserves} ounces."
        return "Insufficient gold reserves."

    def get_gold_reserves(self):
        return self.gold_reserves
