import unittest
import pandas as pd
from io import StringIO
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """
        Set up sample data for testing.
        """
        self.csv_data = StringIO("""
        date,category,value
        2025-04-01,Food,100
        2025-04-02,Transport,50
        2025-04-03,Food,200
        2025-04-04,Entertainment,150
        """)
        self.data = pd.read_csv(self.csv_data)
        self.loader = DataLoader(required_columns=["date", "category", "value"])

    def test_load_csv(self):
        """
        Test that data is loaded correctly from a CSV file.
        """
        loader = DataLoader()
        data = loader.load_csv(self.csv_data)
        self.assertEqual(len(data), 4)
        self.assertListEqual(list(data.columns), ["date", "category", "value"])

    def test_validate_data(self):
        """
        Test validation of required columns.
        """
        validated_data = self.loader.validate_data(self.data)
        self.assertEqual(len(validated_data), 4)

        # Test missing required columns
        loader = DataLoader(required_columns=["nonexistent_column"])
        with self.assertRaises(ValueError) as context:
            loader.validate_data(self.data)
        self.assertIn("Missing required columns", str(context.exception))

    def test_clean_data(self):
        """
        Test data cleaning functionality.
        """
        # Add invalid date and missing value
        self.data.loc[4] = ["invalid_date", "Food", 300]
        self.data.loc[5] = [None, "Transport", None]

        cleaned_data = self.loader.clean_data(self.data)
        self.assertEqual(len(cleaned_data), 4)  # Invalid rows should be dropped
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_data["date"]))

    def test_filter_by_date_range(self):
        """
        Test filtering by date range.
        """
        filtered_data = self.loader.filter_by_date_range(self.data, "2025-04-02", "2025-04-03")
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue((filtered_data["date"] >= "2025-04-02").all())
        self.assertTrue((filtered_data["date"] <= "2025-04-03").all())

    def test_filter_by_categories(self):
        """
        Test filtering by specific categories.
        """
        filtered_data = self.loader.filter_by_categories(self.data, "category", ["Food"])
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue((filtered_data["category"] == "Food").all())

        # Test invalid column
        with self.assertRaises(ValueError) as context:
            self.loader.filter_by_categories(self.data, "nonexistent_column", ["Food"])
        self.assertIn("The DataFrame does not contain the column", str(context.exception))

if __name__ == "__main__":
    unittest.main()