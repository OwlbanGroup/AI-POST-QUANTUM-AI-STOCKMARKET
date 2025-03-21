class OwlbanGroup:
    def __init__(self):
        self.assets_under_management = 0  # Total AUM in dollars
        self.companies = []

    def add_company(self, company_name, aum):
        self.companies.append(company_name)
        self.assets_under_management += aum
        return f"Company {company_name} added. Total AUM is now {self.assets_under_management}."

    def remove_company(self, company_name, aum):
        if company_name in self.companies:
            self.companies.remove(company_name)
            self.assets_under_management -= aum
            return f"Company {company_name} removed. Total AUM is now {self.assets_under_management}."
        return "Company not found."

    def get_aum(self):
        return self.assets_under_management

    def get_companies(self):
        return self.companies
