class FinancialReport:
    def __init__(self, trading_engine, compliance):
        self.trading_engine = trading_engine
        self.compliance = compliance

    def generate_report(self):
        executed_trades = self.trading_engine.orders
        report = {
            "post_quantum_insights": "Insights based on post-quantum analysis will be included here.",
            "total_orders": len(executed_trades),
            "compliance_check": self.compliance.generate_report(),
            "executed_trades": executed_trades,
            "total_executed_trades": len(executed_trades),  # Count of executed trades
            "trade_summary": [{"type": trade['type'], "amount": trade['amount'], "price": trade['price']} for trade in executed_trades]  # Summary of executed trades
        }
        return report
