from utils.adls_reader import read_log_file
from models.detect_anomalies import detect_anomalies
from visualizations.plot_generator import plot_anomalies
import pandas as pd

def main():
    df = read_log_file(
        container="logpredict",
        file_path="logs/sample_logs.csv",
        file_type="csv"
    )

    # Ensure timestamp column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Step 1: Aggregate logs per day
    daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index(name='log_count')
    daily_counts['date'] = pd.to_datetime(daily_counts['timestamp'])
    daily_counts.drop(columns=['timestamp'], inplace=True)

    # Step 2: Run anomaly detection
    anomaly_df = detect_anomalies(daily_counts, column='log_count')

    # Step 3: Visualize
    plot_anomalies(anomaly_df, time_column='date', value_column='log_count')

if __name__ == "__main__":
    main()