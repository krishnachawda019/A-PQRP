import pandas as pd
import numpy as np 

def get_dataset_summary(df):
    rows, columns = df.shape #to get tuple of rows and columns count
    memory_usage = df.memory_usage(deep = True).sum() #to display memory usage
    summary = {"Rows" : int(rows) , "Columns" : int(columns) , "Memory Usage" : int(df.memory_usage(deep = True).sum())}
    return summary
    

def get_missing_values(df):
    result = df.isnull().sum().to_dict()
    return result

def get_duplicate_count(df):
    duplicate_count = int(df.duplicated().sum())
    return {
        "Duplicate Rows" : duplicate_count
    }

def get_data_types(df):
    data_type_dict = df.dtypes.astype(str).to_dict()
    return data_type_dict

def get_basic_statistics(df):
    statistics = df.describe().to_dict()
    return statistics

def get_numeric_columns(df):
    numeric_df = df.select_dtypes(include = "number").columns.tolist()
    return {
        "Numeric Columns" : numeric_df
    }
    
def get_categorical_columns(df):
    categorical_columns = df.select_dtypes(include = ['object' , 'category']).columns.tolist()
    return {
        "Categorical Columns" : categorical_columns
    }

def get_unique_values(df):
    unique_values = df.nunique().to_dict()
    return {
        "Unique Values" : unique_values
    }

def generate_profile(df):
    return{
        "summary" : get_dataset_summary(df),
        "missing_values" : get_missing_values(df),
        "duplicate_count" : get_duplicate_count(df),
        "data_types" : get_data_types(df),
        "basic_statistics" : get_basic_statistics(df),
        "numeric_columns" : get_numeric_columns(df),
        "categorical_columns" : get_categorical_columns(df),
        "unique_values" : get_unique_values(df)
    }
