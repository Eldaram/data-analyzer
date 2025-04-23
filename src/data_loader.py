import pandas as pd
from typing import List, Optional

class DataLoader:
    def __init__(self, required_columns: Optional[List[str]] = None):
        """
        Initialize the DataLoader with optional required columns.
        :param required_columns: List of column names that must be present in the data.
        """
        self.required_columns = required_columns

    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load a CSV file into a pandas DataFrame.
        :param file_path: Path to the CSV file.
        :return: Loaded DataFrame.
        """
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {e}")

    def validate_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate the DataFrame by checking for required columns and handling missing values.
        :param data: DataFrame to validate.
        :return: Validated DataFrame.
        """
        if self.required_columns:
            missing_columns = [col for col in self.required_columns if col not in data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

        # Handle missing values (example: drop rows with missing values)
        data = data.dropna()
        return data

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Perform basic data cleaning such as date parsing and type conversion.
        :param data: DataFrame to clean.
        :return: Cleaned DataFrame.
        """
        # Example: Convert 'date' column to datetime if it exists
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'], errors='coerce')
            data = data.dropna(subset=['date'])  # Drop rows where 'date' could not be parsed

        # Example: Convert numeric columns to appropriate types
        for col in data.select_dtypes(include=['object']).columns:
            try:
                data[col] = pd.to_numeric(data[col], errors='ignore')
            except Exception:
                pass

        return data

    def filter_by_date_range(self, data: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter the DataFrame by a date range.
        :param data: DataFrame to filter.
        :param start_date: Start date (inclusive) in 'YYYY-MM-DD' format.
        :param end_date: End date (inclusive) in 'YYYY-MM-DD' format.
        :return: Filtered DataFrame.
        """
        if 'date' not in data.columns:
            raise ValueError("The DataFrame does not contain a 'date' column.")

        mask = (data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))
        return data.loc[mask]

    def filter_by_categories(self, data: pd.DataFrame, column: str, categories: List[str]) -> pd.DataFrame:
        """
        Filter the DataFrame by specific categories in a column.
        :param data: DataFrame to filter.
        :param column: Column name to filter by.
        :param categories: List of categories to include.
        :return: Filtered DataFrame.
        """
        if column not in data.columns:
            raise ValueError(f"The DataFrame does not contain the column '{column}'.")

        return data[data[column].isin(categories)]

