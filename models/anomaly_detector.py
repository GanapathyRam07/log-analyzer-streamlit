# models/anomaly_detector.py
import pandas as pd
from models.detect_anomalies import detect_anomalies  # Use the reusable function

def run_anomaly_detection(df: pd.DataFrame) -> pd.DataFrame:
    # Convert timestamp to date
    df['date'] = pd.to_datetime(df['timestamp']).dt.date

    # Group by date to count logs
    daily_counts = df.groupby('date').size().reset_index(name='log_count')

    # Use the reusable anomaly detection function
    result = detect_anomalies(daily_counts, column='log_count')
    
    return result