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
    statistics = df.describe().where(pd.notnull(df.describe()), None).to_dict()
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

def get_correlation_matrix(df):
    correlation_matrix = df.select_dtypes(include = "number").corr().to_dict()
    return {
        "correlation_matrix" : correlation_matrix
    }

def detect_outliers(df):
    numeric_df = df.select_dtypes(include = "number")
    dict_1 = {}
    for column in numeric_df.columns :
        series = numeric_df[column].dropna()
        if series.empty :
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier = series[(series < lower_bound) | (series > upper_bound)].tolist()
        dict_1[column] = {"count" : len(outlier),
                          "values" : outlier ,
                          "lower_bound" : lower_bound,
                          "Upper_bound" : upper_bound}
    return {
        "outlier" : dict_1
    }
        
def get_data_quality_score(df):
    issues = []
    outlier_columns = 0
    missing_percentage = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
    if missing_percentage != 0:
        issues.append("Missing Values Detected")
    quality_score = 100 - missing_percentage
    duplicate_percentage = (df.duplicated().sum() / df.shape[0]) * 100
    if duplicate_percentage != 0:
        issues.append("Duplicate Values Detected")
    quality_score -= duplicate_percentage
    numeric_df = df.select_dtypes(include = "number")
    for column in numeric_df.columns :
        series = numeric_df[column].dropna()
        if series.empty :
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier = series[(series < lower_bound) | (series > upper_bound)].tolist()
        if len(outlier) > 0:
            outlier_columns += 1
    outlier_percentage = (outlier_columns / len(numeric_df.columns)) * 100
    if outlier_percentage != 0:
        issues.append("Outliers Detected")
    quality_score -= outlier_percentage
    if not issues :
        issues.append("No data quality issues detected")
    return {
        "qualtiy_score" : max(0 ,round(quality_score,2)),
        "missing_percentage" : missing_percentage,
        "duplicate_percentage" : duplicate_percentage,
        "outlier_percentage" : outlier_percentage,
        "issues" : issues
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
        "unique_values" : get_unique_values(df),
        "corrlation_matrix" : get_correlation_matrix(df),
        "detect_outliers" : detect_outliers(df),
        "data_quality_score" : get_data_quality_score(df)
    }



