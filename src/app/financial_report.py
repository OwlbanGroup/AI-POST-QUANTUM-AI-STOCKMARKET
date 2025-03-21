class FinancialReport:
    def __init__(self, trading_engine, compliance):
        self.trading_engine = trading_engine
        self.compliance = compliance

    def generate_report(self):
        report = {
            "total_orders": len(self.trading_engine.orders),
            "compliance_check": self.compliance.generate_report(),
            "executed_trades": self.trading_engine.orders
        }
        return report
