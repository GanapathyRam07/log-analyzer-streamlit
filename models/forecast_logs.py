import pandas as pd
from prophet import Prophet

def forecast_log_volume(df: pd.DataFrame, periods: int = 7) -> pd.DataFrame:
    # Prepare data for Prophet
    daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index(name='log_count')
    daily_counts.columns = ['ds', 'y']

    model = Prophet()
    model.fit(daily_counts)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Keep only the relevant columns
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]