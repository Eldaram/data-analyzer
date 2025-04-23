import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional

class DataVisualizer:
    def __init__(self):
        """
        Initialize the DataVisualizer class.
        """
        pass

    def bar_chart(self, data: pd.DataFrame, category_column: str, value_column: str, title: str = "Bar Chart", 
                  color: str = "blue", save_path: Optional[str] = None):
        """
        Generate a bar chart for spending by category.
        :param data: DataFrame containing the data.
        :param category_column: Column containing categories.
        :param value_column: Column containing values.
        :param title: Title of the chart.
        :param color: Color of the bars.
        :param save_path: Path to save the chart as a file.
        :return: Matplotlib figure.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=category_column, y=value_column, data=data, ax=ax, color=color)
        ax.set_title(title)
        ax.set_xlabel(category_column)
        ax.set_ylabel(value_column)
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path)
        return fig

    def line_chart(self, data: pd.DataFrame, x_column: str, y_column: str, title: str = "Line Chart", 
                   color: str = "blue", save_path: Optional[str] = None):
        """
        Generate a line chart for spending over time.
        :param data: DataFrame containing the data.
        :param x_column: Column for the x-axis (e.g., dates).
        :param y_column: Column for the y-axis (e.g., values).
        :param title: Title of the chart.
        :param color: Color of the line.
        :param save_path: Path to save the chart as a file.
        :return: Matplotlib figure.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=x_column, y=y_column, data=data, ax=ax, color=color)
        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        
        if save_path:
            plt.savefig(save_path)
        return fig

    def pie_chart(self, data: pd.DataFrame, value_column: str, label_column: str, title: str = "Pie Chart", 
                  save_path: Optional[str] = None):
        """
        Generate a pie chart for spending distribution.
        :param data: DataFrame containing the data.
        :param value_column: Column containing values.
        :param label_column: Column containing labels.
        :param title: Title of the chart.
        :param save_path: Path to save the chart as a file.
        :return: Matplotlib figure.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(data[value_column], labels=data[label_column], autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path)
        return fig

    def heatmap(self, data: pd.DataFrame, title: str = "Heatmap", cmap: str = "coolwarm", 
                save_path: Optional[str] = None):
        """
        Generate a heatmap for correlation between variables.
        :param data: DataFrame containing the data.
        :param title: Title of the heatmap.
        :param cmap: Colormap for the heatmap.
        :param save_path: Path to save the heatmap as a file.
        :return: Matplotlib figure.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=cmap, ax=ax)
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path)
        return fig