import argparse
import pandas as pd
from src.data_loader import DataLoader
from src.analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Data Analyzer CLI")
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    parser.add_argument("--analysis", type=str, choices=["summary", "time-series", "category", "segmentation"], 
                        help="Type of analysis to perform")
    parser.add_argument("--plot", type=str, choices=["bar", "line", "pie", "heatmap"], 
                        help="Type of plot to generate")
    parser.add_argument("--output", type=str, help="Path to save the analysis or plot result")
    parser.add_argument("--start_date", type=str, help="Start date for time-series analysis (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="End date for time-series analysis (YYYY-MM-DD)")
    parser.add_argument("--category_column", type=str, default="category", 
                        help="Column name for category-based analysis (default: 'category')")
    parser.add_argument("--value_column", type=str, default="amount", 
                        help="Column name for value-based analysis (default: 'amount')")
    parser.add_argument("--top_n", type=int, default=5, help="Number of top categories to display (default: 5)")
    args = parser.parse_args()

    # Load and validate data
    loader = DataLoader(required_columns=["date", "category", "amount", "customer_id"])
    try:
        data = loader.load_csv(args.file_path)
        data = loader.validate_data(data)
        data = loader.clean_data(data)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Perform analysis
    analyzer = DataAnalyzer(data)
    analysis_result = None
    if args.analysis == "summary":
        analysis_result = analyzer.summary_statistics(args.category_column, args.value_column)
    elif args.analysis == "time-series":
        if not args.start_date or not args.end_date:
            print("Error: --start_date and --end_date are required for time-series analysis.")
            return
        analysis_result = analyzer.time_series_analysis("date", args.value_column)
    elif args.analysis == "category":
        analysis_result = analyzer.top_spending_categories(args.category_column, args.value_column, args.top_n)
    elif args.analysis == "segmentation":
        analysis_result = analyzer.customer_segmentation("customer_id", args.value_column)

    # Save analysis result if specified
    if analysis_result is not None:
        print("Analysis Result:")
        print(analysis_result)
        if args.output:
            analysis_result.to_csv(args.output, index=False)
            print(f"Analysis result saved to {args.output}")

    # Generate visualization
    visualizer = DataVisualizer()
    if args.plot == "bar":
        fig = visualizer.bar_chart(data, args.category_column, args.value_column, title="Bar Chart", save_path=args.output)
    elif args.plot == "line":
        fig = visualizer.line_chart(data, "date", args.value_column, title="Line Chart", save_path=args.output)
    elif args.plot == "pie":
        fig = visualizer.pie_chart(data, args.value_column, args.category_column, title="Pie Chart", save_path=args.output)
    elif args.plot == "heatmap":
        fig = visualizer.heatmap(data, title="Heatmap", save_path=args.output)

    print("Visualization generated successfully.")
    if args.output:
        print(f"Visualization saved to {args.output}")

if __name__ == "__main__":
    main()