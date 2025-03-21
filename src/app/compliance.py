class Compliance:
    def __init__(self):
        self.regulations = []

    def add_regulation(self, regulation):
        self.regulations.append(regulation)
        return f"Regulation added: {regulation}"

    def check_compliance(self, transaction):
        # Placeholder for compliance checking logic
        # For simplicity, we'll assume all transactions are compliant
        return True

    def generate_report(self):
        report = {
            "total_regulations": len(self.regulations),
            "regulations": self.regulations
        }
        return report
