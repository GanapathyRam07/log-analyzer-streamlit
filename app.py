# app.py
import streamlit as st
import pandas as pd
import json
from utils.adls_reader import read_log_file
from models.anomaly_detector import detect_anomalies
from visualizations.plot_generator import plot_anomalies

st.title("Log Analyzer and Anomaly Detector")

# Upload / Input
container = st.text_input("Enter ADLS Container Name")
file_path = st.text_input("Enter File Path in ADLS (e.g., logs/log_data.csv)")

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
        else:
            st.success("Logs loaded successfully.")
            st.dataframe(df, use_container_width=True, height=500)

            # Ensure timestamp is datetime
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            else:
                st.error("Missing 'timestamp' column in data.")
                st.stop()

            result_df = detect_anomalies(df)
            st.subheader("Anomaly Detection Results")
            st.dataframe(result_df, use_container_width=True, height=400)

            st.subheader("Anomaly Chart")
            plot_anomalies(result_df, time_col='date', value_col='log_count')

    except Exception as e:
        st.error(f"Error: {e}")