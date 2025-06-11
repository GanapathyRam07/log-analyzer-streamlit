# test_anomaly.py
import pandas as pd
from models.anomaly_detector import run_anomaly_detection

# Sample log data
data = {
    "timestamp": [
        "2025-06-01 12:00", "2025-06-01 13:00",
        "2025-06-02 12:00", "2025-06-02 13:00",
        "2025-06-03 14:00", 
        "2025-06-10 10:00", "2025-06-10 11:00", "2025-06-10 12:00",  # Add multiple logs for 10th
        "2025-06-10 13:00", "2025-06-10 14:00", "2025-06-10 15:00",
        "2025-06-10 16:00", "2025-06-10 17:00"
    ]
}
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Run anomaly detection
result = run_anomaly_detection(df)
print(result)