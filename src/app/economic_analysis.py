class EconomicAnalysis:
    def __init__(self):
        self.indicators = {}

    def add_indicator(self, name, value):
        self.indicators[name] = value
        return f"Indicator added: {name} with value {value}"

    def analyze_economy(self):
        # Enhanced economic analysis logic
        analysis = {}
        for name, value in self.indicators.items():
            # Example logic: categorize indicators based on their values
            if value > 0:
                analysis[name] = "Positive"
            elif value < 0:
                analysis[name] = "Negative"
            else:
                analysis[name] = "Neutral"
        return analysis

    def remove_indicator(self, name):
        if name in self.indicators:
            del self.indicators[name]
            return f"Indicator removed: {name}"
        return f"Indicator not found: {name}"

    def update_indicator(self, name, new_value):
        if name in self.indicators:
            self.indicators[name] = new_value
            return f"Indicator updated: {name} to {new_value}"
        return f"Indicator not found: {name}"

    def generate_report(self):
        report = {
            "total_indicators": len(self.indicators),
            "indicators": self.indicators,
            "analysis": self.analyze_economy()
        }
        return report

    def generate_report(self):
        report = {
            "total_indicators": len(self.indicators),
            "indicators": self.indicators
        }
        return report
