# # visualizations/plot_generator.py
# import matplotlib.pyplot as plt

# def plot_anomalies(df, time_column="timestamp", value_column="error_count"):
#     plt.figure(figsize=(12, 6))
#     plt.plot(df[time_column], df[value_column], label="Log Value")
#     plt.scatter(df[df["anomaly"] == 1][time_column], df[df["anomaly"] == 1][value_column],
#                 color="red", label="Anomaly", marker="x")
#     plt.xlabel("Time")
#     plt.ylabel("Errors/Metric")
#     plt.title("Log Anomalies Over Time")
#     plt.legend()
#     plt.grid()
#     plt.tight_layout()
#     plt.show()# visualizations/plot_generator.py
import matplotlib.pyplot as plt
import streamlit as st

def plot_anomalies(df, time_col='date', value_col='log_count'):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the main log values
    ax.plot(df[time_col], df[value_col], label='Log Value', color='blue', marker='o')
    
    # Highlight anomalies
    anomalies = df[df['anomaly'] == 1]
    ax.scatter(anomalies[time_col], anomalies[value_col], color='red', label='Anomaly', marker='x', s=100)

    ax.set_title("Log Anomalies Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Errors / Metric")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
