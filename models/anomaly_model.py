import pandas as pd
from pyod.models.iforest import IForest

def detect_anomalies(df: pd.DataFrame, value_column: str = "error_count"):
    # Prepare data
    X = df[[value_column]].values

    # Fit isolation forest
    model = IForest(contamination=0.1)
    model.fit(X)

    df["anomaly"] = model.predict(X)  # 1 = anomaly, 0 = normal
    return df