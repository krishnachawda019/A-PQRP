import os
import pandas as pd

def process_file(file_path: str):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        df = pd.read_csv(file_path)
    elif extension == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported File Format")
    return{
        "filename": os.path.basename(file_path),
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "status": "success"
    }

