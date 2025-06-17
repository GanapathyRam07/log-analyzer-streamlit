# app.py
import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from utils.adls_reader import read_log_file
from models.anomaly_detector import detect_anomalies
from visualizations.plot_generator import plot_anomalies
from models.forecast_logs import forecast_log_volume

st.set_page_config(page_title="Log Analyzer", layout="wide")
st.title("📊 Log Analyzer and Anomaly Detector")

# Upload / Input
container = st.text_input("Enter ADLS Container Name")
file_path = st.text_input("Enter File Path in ADLS (e.g., logs/log_data.csv)")

# JSON Parser Function
def parse_json_logs(content: str) -> pd.DataFrame:
    try:
        lines = content.strip().split('\n')
        records = [json.loads(line) for line in lines]
        df = pd.DataFrame(records)
        return df
    except Exception as e:
        st.error(f"Failed to parse JSON: {e}")
        return pd.DataFrame()

if st.button("Analyze Logs"):
    try:
        file_type = "json" if file_path.endswith(".json") else "csv"
        content = read_log_file(container, file_path, file_type=file_type)

        # Parse based on file type
        if file_type == "json":
            df = parse_json_logs(content)
        else:
            df = content  # already a DataFrame

        if df.empty:
            st.warning("No data found or failed to parse file.")
            st.stop()

        st.success("Logs loaded successfully.")
        st.dataframe(df, use_container_width=True, height=500)

        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        else:
            st.error("Missing 'timestamp' column in data.")
            st.stop()

        # Anomaly Detection
        result_df = detect_anomalies(df)
        st.subheader("🚨 Anomaly Detection Results")
        st.dataframe(result_df, use_container_width=True, height=400)

        st.subheader("📈 Anomaly Trend")
        plot_anomalies(result_df, time_col='date', value_col='log_count')

        # Forecast Log Volume (Step 4)
        st.subheader("📉 Forecasting Future Log Volumes")

        if len(df) < 30:
            st.warning("⚠️ Not enough log data (minimum ~30 entries recommended) for accurate forecasting.")
        else:
            forecast_df = forecast_log_volume(df)

            st.dataframe(forecast_df.tail(7), use_container_width=True, height=250)

            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(forecast_df['ds'], forecast_df['yhat'], label="Predicted Log Count", color='blue')
            ax1.fill_between(forecast_df['ds'], forecast_df['yhat_lower'], forecast_df['yhat_upper'],
                             color='skyblue', alpha=0.3, label='Confidence Interval')
            ax1.set_title("Forecasted Log Volume")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Log Count")
            ax1.legend()
            st.pyplot(fig1)

            # Step 5: Compare Actual vs Forecasted
            st.subheader("🔍 Compare Actual vs Forecasted Logs")

            actual_df = df.groupby(df['timestamp'].dt.date).size().reset_index(name='actual')
            actual_df.columns = ['ds', 'actual']

            merged = pd.merge(forecast_df, actual_df, on='ds', how='left')

            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.bar(merged['ds'], merged['actual'], label="Actual Logs", alpha=0.6, color='gray')
            ax2.plot(merged['ds'], merged['yhat'], color='red', label="Forecasted Logs", linewidth=2)
            ax2.set_title("Actual vs Forecasted Log Volume")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Log Count")
            ax2.legend()
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"Error: {e}")