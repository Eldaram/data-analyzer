import pandas as pd
from typing import List, Dict

class DataAnalyzer:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataAnalyzer with a DataFrame.
        :param data: DataFrame to analyze.
        """
        self.data = data

    def summary_statistics(self, category_column: str, value_column: str) -> pd.DataFrame:
        """
        Calculate summary statistics (mean, median, std dev) grouped by a category.
        :param category_column: Column to group by.
        :param value_column: Column to calculate statistics for.
        :return: DataFrame with summary statistics.
        """
        if category_column not in self.data.columns or value_column not in self.data.columns:
            raise ValueError(f"Columns '{category_column}' or '{value_column}' not found in the DataFrame.")
        
        return self.data.groupby(category_column)[value_column].agg(['mean', 'median', 'std']).reset_index()

    def time_series_analysis(self, date_column: str, value_column: str) -> pd.DataFrame:
        """
        Analyze spending trends over time.
        :param date_column: Column containing date values.
        :param value_column: Column to analyze over time.
        :return: DataFrame with spending trends over time.
        """
        if date_column not in self.data.columns or value_column not in self.data.columns:
            raise ValueError(f"Columns '{date_column}' or '{value_column}' not found in the DataFrame.")
        
        self.data[date_column] = pd.to_datetime(self.data[date_column], errors='coerce')
        return self.data.groupby(date_column)[value_column].sum().reset_index()

    def spending_distribution(self, value_column: str, bins: int = 10) -> pd.DataFrame:
        """
        Analyze spending distribution by dividing values into bins.
        :param value_column: Column to analyze.
        :param bins: Number of bins for distribution.
        :return: DataFrame with spending distribution.
        """
        if value_column not in self.data.columns:
            raise ValueError(f"Column '{value_column}' not found in the DataFrame.")
        
        self.data['spending_bin'] = pd.cut(self.data[value_column], bins=bins)
        return self.data['spending_bin'].value_counts().reset_index().rename(columns={'index': 'Range', 'spending_bin': 'Count'})

    def top_spending_categories(self, category_column: str, value_column: str, top_n: int = 5) -> pd.DataFrame:
        """
        Identify the top spending categories.
        :param category_column: Column containing categories.
        :param value_column: Column containing spending values.
        :param top_n: Number of top categories to return.
        :return: DataFrame with top spending categories.
        """
        if category_column not in self.data.columns or value_column not in self.data.columns:
            raise ValueError(f"Columns '{category_column}' or '{value_column}' not found in the DataFrame.")
        
        return self.data.groupby(category_column)[value_column].sum().nlargest(top_n).reset_index()

    def customer_segmentation(self, customer_column: str, value_column: str) -> pd.DataFrame:
        """
        Segment customers by their spending patterns.
        :param customer_column: Column containing customer identifiers.
        :param value_column: Column containing spending values.
        :return: DataFrame with customer segmentation.
        """
        if customer_column not in self.data.columns or value_column not in self.data.columns:
            raise ValueError(f"Columns '{customer_column}' or '{value_column}' not found in the DataFrame.")
        
        return self.data.groupby(customer_column)[value_column].agg(['sum', 'mean', 'count']).reset_index().rename(
            columns={'sum': 'Total Spending', 'mean': 'Average Spending', 'count': 'Transaction Count'}
        )