import unittest
import pandas as pd
from io import StringIO
from src.visualizer import DataVisualizer
import os

class TestDataVisualizer(unittest.TestCase):
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
        self.visualizer = DataVisualizer()
        self.test_output_path = "test_output.png"

    def tearDown(self):
        """
        Clean up any generated files after tests.
        """
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_bar_chart(self):
        """
        Test bar chart generation.
        """
        fig = self.visualizer.bar_chart(self.data, "category", "amount", save_path=self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))  # Check if the file was saved
        self.assertIsNotNone(fig)  # Ensure the figure is generated

    def test_line_chart(self):
        """
        Test line chart generation.
        """
        fig = self.visualizer.line_chart(self.data, "date", "amount", save_path=self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))  # Check if the file was saved
        self.assertIsNotNone(fig)  # Ensure the figure is generated

    def test_pie_chart(self):
        """
        Test pie chart generation.
        """
        fig = self.visualizer.pie_chart(self.data, "amount", "category", save_path=self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))  # Check if the file was saved
        self.assertIsNotNone(fig)  # Ensure the figure is generated

    def test_heatmap(self):
        """
        Test heatmap generation.
        """
        fig = self.visualizer.heatmap(self.data, save_path=self.test_output_path)
        self.assertTrue(os.path.exists(self.test_output_path))  # Check if the file was saved
        self.assertIsNotNone(fig)  # Ensure the figure is generated

if __name__ == "__main__":
    unittest.main()