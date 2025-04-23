import unittest
import pandas as pd
from io import StringIO
from src.analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Set up sample data for testing.
        """
        self.csv_data = StringIO("""
        date,category,amount,customer_id
        2025-04-01,Food,100,C1
        2025-04-02,Transport,50,C2
        2025-04-03,Food,200,C1
        2025-04-04,Entertainment,150,C3
        2025-04-05,Transport,75,C2
        """)
        self.data = pd.read_csv(self.csv_data)
        self.analyzer = DataAnalyzer(self.data)

    def test_summary_statistics(self):
        """
        Test summary statistics calculation.
        """
        result = self.analyzer.summary_statistics("category", "amount")
        self.assertEqual(len(result), 3)  # 3 unique categories
        self.assertIn("mean", result.columns)
        self.assertIn("median", result.columns)
        self.assertIn("std", result.columns)

    def test_time_series_analysis(self):
        """
        Test time-series analysis.
        """
        result = self.analyzer.time_series_analysis("date", "amount")
        self.assertEqual(len(result), 5)  # 5 unique dates
        self.assertIn("date", result.columns)
        self.assertIn("amount", result.columns)

    def test_spending_distribution(self):
        """
        Test spending distribution analysis.
        """
        result = self.analyzer.spending_distribution("amount", bins=3)
        self.assertEqual(len(result), 3)  # 3 bins
        self.assertIn("Range", result.columns)
        self.assertIn("Count", result.columns)

    def test_top_spending_categories(self):
        """
        Test top spending categories identification.
        """
        result = self.analyzer.top_spending_categories("category", "amount", top_n=2)
        self.assertEqual(len(result), 2)  # Top 2 categories
        self.assertIn("category", result.columns)
        self.assertIn("amount", result.columns)

    def test_customer_segmentation(self):
        """
        Test customer segmentation.
        """
        result = self.analyzer.customer_segmentation("customer_id", "amount")
        self.assertEqual(len(result), 3)  # 3 unique customers
        self.assertIn("Total Spending", result.columns)
        self.assertIn("Average Spending", result.columns)
        self.assertIn("Transaction Count", result.columns)

    def test_invalid_columns(self):
        """
        Test handling of invalid columns.
        """
        with self.assertRaises(ValueError) as context:
            self.analyzer.summary_statistics("invalid_column", "amount")
        self.assertIn("Columns 'invalid_column' or 'amount' not found", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.analyzer.time_series_analysis("invalid_column", "amount")
        self.assertIn("Columns 'invalid_column' or 'amount' not found", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.analyzer.spending_distribution("invalid_column")
        self.assertIn("Column 'invalid_column' not found", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.analyzer.top_spending_categories("invalid_column", "amount")
        self.assertIn("Columns 'invalid_column' or 'amount' not found", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.analyzer.customer_segmentation("invalid_column", "amount")
        self.assertIn("Columns 'invalid_column' or 'amount' not found", str(context.exception))

if __name__ == "__main__":
    unittest.main()