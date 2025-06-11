from utils.adls_reader import read_log_file

df = read_log_file(
    container="logpredict",
    file_path="logs/sample_logs.csv",
    file_type="csv"
)

print(df)