from flask import render_template
from .financial_report import FinancialReport

class ReportingInterface:
    def __init__(self, trading_engine, compliance):
        self.financial_report = FinancialReport(trading_engine, compliance)

    def display_report(self):
        report = self.financial_report.generate_report()
        return render_template('financial_report.html', report=report)
