# models/detect_anomalies.py
from pyod.models.iforest import IForest
import pandas as pd

def detect_anomalies(df: pd.DataFrame, column: str = 'log_count') -> pd.DataFrame:
    model = IForest()
    model.fit(df[[column]])
    df['anomaly'] = model.predict(df[[column]])
    return df