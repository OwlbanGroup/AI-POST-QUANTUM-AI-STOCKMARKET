import unittest
from natural_resources_management import NaturalResourcesManagement
from src.data.data_loader import DataLoader
from src.data.data_preprocessing import DataPreprocessor

class TestNaturalResourcesManagement(unittest.TestCase):
    def setUp(self):
        self.manager = NaturalResourcesManagement()
        self.manager.add_resource("Water", 100)
        self.manager.add_resource("Gold", 50)

    def test_add_resource(self):
        result = self.manager.add_resource("Silver", 30)
        self.assertEqual(result, "Resource added: Silver with quantity 30")
        self.assertIn("Silver", self.manager.resources)

    def test_generate_report(self):
        report = self.manager.generate_report()
        self.assertEqual(report["total_resources"], 2)
        self.assertIn("Water", report["resources"])
        self.assertIn("Gold", report["resources"])

    def test_analyze_historical_data(self):
        historical_data = {"Water": [100, 90, 80], "Gold": [50, 55, 60]}
        report = self.manager.generate_report(historical_data=historical_data)
        self.assertIn("historical_analysis", report)

if __name__ == "__main__":
    unittest.main()
