import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER=localhost;"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID=sa;"
        f"PWD={os.environ['MSSQL_SA_PASSWORD']};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)