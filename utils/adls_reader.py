# import os
# import pandas as pd
# from azure.identity import DefaultAzureCredential
# from azure.storage.filedatalake import DataLakeServiceClient
# from io import StringIO

# def get_adls_client():
#     account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
#     if not account_name:
#         raise EnvironmentError("AZURE_STORAGE_ACCOUNT_NAME not set.")

#     credential = DefaultAzureCredential()
#     service_client = DataLakeServiceClient(
#         account_url=f"https://{account_name}.dfs.core.windows.net",
#         credential=credential
#     )
#     return service_client

# def read_log_file(container: str, file_path: str, file_type: str = "csv") -> pd.DataFrame:
#     service_client = get_adls_client()
#     file_system_client = service_client.get_file_system_client(file_system=container)
#     file_client = file_system_client.get_file_client(file_path)

#     download = file_client.download_file()
#     content = download.readall().decode()

#     if file_type == "csv":
#         return pd.read_csv(StringIO(content))
#     elif file_type == "json":
#         return pd.read_json(StringIO(content), lines=True)
#     else:
#         raise ValueError("Unsupported file type. Use 'csv' or 'json'.")# utils/adls_reader.py
import os
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from io import StringIO

def get_adls_client():
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    if not account_name:
        raise EnvironmentError("AZURE_STORAGE_ACCOUNT_NAME not set.")

    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=credential
    )
    return service_client

def read_log_file(container: str, file_path: str, file_type: str = "csv"):
    service_client = get_adls_client()
    file_system_client = service_client.get_file_system_client(file_system=container)
    file_client = file_system_client.get_file_client(file_path)

    download = file_client.download_file()
    content = download.readall().decode()

    if file_type == "csv":
        return pd.read_csv(StringIO(content))
    elif file_type == "json":
        return content  # return raw string for parsing in app
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'json'.")
