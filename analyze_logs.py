import pandas as pd
from utils.adls_reader import read_log_file
from models.anomaly_model import detect_anomalies
from visualizations.plot_generator import plot_anomalies

# Step 1: Read the log data
df = read_log_file(
    container="logpredict",
    file_path="2025-06-10/logs_today.csv",  # adjust as needed
    file_type="csv"
)

# Step 2: Detect anomalies in the log values
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = detect_anomalies(df, value_column="error_count")  # or whatever column is numeric

# Step 3: Plot anomalies
plot_anomalies(df)