# test_pandas.py
import pandas as pd

df = pd.DataFrame({
    "timestamp": ["2025-06-09 12:00", "2025-06-10 12:00"],
    "level": ["ERROR", "INFO"],
    "message": ["Something failed", "System running fine"]
})

print(df)