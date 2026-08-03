import pandas as pd
import numpy as np 

PRICE_ALIASES = {"open" : ["open" ,"opening_price" ,"open_price" ,"opening"],
                 "high" : ["high" ,"high_price" ,"high price"],
                 "low" : ["low" ,"low price" ,"low_price"],
                 "close" : ["close" ,"closing_price" ,"close_price" ,"closing"],
                 "adjusted_close" : ["adj close" ,"adjusted_close" ,"adj_close" ,"adjusted close"],
                 "vwap" : ["vwap" ,"volume weight average price" ,"volume_weight_average_price"] }

VOLUME_ALIASES = {"volume" : ["volume" ,"trading volume" ,"trade volume"],
                  "shares_traded" : ["shares traded" ,"total traded quantity" ,"traded_quantity" ,"quantity"],
                  "turnover" : ["turn over" ,"value traded" ,"traded value"]}

TARGET_PRIORITY = {"returns" :{"aliases" : ["returns" ,"return" ,"next_day_return" ,"future_return"],
                               "confidence" : "High",
                               "reason" :"Engineered return column detected" },
                   "adjusted_close" : {"aliases" : ["adj close" ,"adjusted_close" ,"close" ,"closing_price" ,"target" ,"label"],
                                       "confidence" : "High",
                                       "reason" :"Engineered return column detected" },
                   "target" : {"aliases" : ["target" ,"label" ,"y"],
                               "confidence" : ["Medium"],
                               "reason" : "Generic target column detected"} }
 
MARKET_ALIASES = {"gdp_growth" : ["gdp growth" ,"gdp" ,"gdp growth (%)"],
                  "inflation" : ["inflation" ,"inflation rate" ,"inflation (%)" ,"cpi"],
                  "interest_rate" : ["interest rate" ,"repo rate" ,"bank rate" ,"policy rate"],
                  "exchange_rate" : ["exchange rate" ,"usd inr" ,"usd/inr" ,"inr/usd" ,"forex"],
                  "sensex" : ["sensex" ,"bse" ,"bse sensex"],
                  "nifty" : ["nifty" ,"nifty 50" ,"nse"],
                  "gold_price" : ["gold" ,"gold price"],
                  "crude_oil" : ["crude oil" ,"oil price" ,"brent" ,"wti"]}

TEXT_KEYWORDS = ["news", "description", "comment", "remarks", "report","summary", "analysis", "headline"]

BOOLEAN_ALIASES = [{"true", "false"}, {"yes", "no"}, {"y", "n"}, {"1", "0"}, {"buy", "sell"}, {"long", "short"}, {"bullish", "bearish"}, {"active", "inactive"}]

HIGH_CARDINALITY_THRESHOLD = 90
MINIMUM_ROWS_FOR_CARDINALITY = 30

def get_dataset_summary(df):
    rows, columns = df.shape #to get tuple of rows and columns count
    dataset_summary = {"Rows" : int(rows) , "Columns" : int(columns) , "Memory Usage" : int(df.memory_usage(deep = True).sum())}
    return dataset_summary
    
def get_missing_values(df):
    result = df.isnull().sum().to_dict()
    return {"missing values" : result}

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
    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        missing_percentage = 0
    else:
        missing_percentage = (
        df.isnull().sum().sum() / total_cells
    ) * 100
    if missing_percentage != 0:
        issues.append("Missing Values Detected")
    quality_score = 100 - missing_percentage
    if df.shape[0] == 0:
        duplicate_percentage = 0
    else:
        duplicate_percentage = (
        df.duplicated().sum() / df.shape[0]
    ) * 100
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
    if len(numeric_df.columns) == 0:
        outlier_percentage = 0
    else:
        outlier_percentage = (outlier_columns / len(numeric_df.columns)) * 100
    if outlier_percentage != 0:
        issues.append("Outliers Detected")
    quality_score -= outlier_percentage
    if not issues :
        issues.append("No data quality issues detected")
    return {
        "quality_score" : max(0 ,round(quality_score,2)),
        "missing_percentage" : missing_percentage,
        "duplicate_percentage" : duplicate_percentage,
        "outlier_percentage" : outlier_percentage,
        "issues" : issues
    }

def safe_value(value):
    value = None if pd.isna(value) else value 
    if value is not None :
        return float(value)
    else :
        return value
def get_distribution_analysis(df):
    dict_1 = {}
    numeric_df = df.select_dtypes(include = "number")
    for column in numeric_df.columns :
        series = numeric_df[column].dropna()
        if series.empty :
            continue
        mean = series.mean()
        median = series.median()
        std = series.std()
        variance = series.var()
        skewness = series.skew()
        kurtosis = series.kurt()        
        dict_1[column] = {"mean" : safe_value(mean),
                          "median" : safe_value(median) ,
                          "standard_deviation" : safe_value(std),
                          "variance" : safe_value(variance),
                          "skewness" : safe_value(skewness),
                          "kurtosis" : safe_value(kurtosis)}
    return {
        "distribution_analysis" : dict_1
    }

def detect_time_column(df):
    dict_1 = {}
    time_keyword = ["date" ,"time" ,"timestamp" ,"year" ,"month" ,"quarter" ,"week" ,"day" ,"trading_date" ,"trade_date" ,"fiscal_year" ,"financial_year" ,"report_date"]
    for column in df.columns :
        column_name = column.lower()
        is_datetime = pd.api.types.is_datetime64_dtype(df[column])
        is_keyword = any(keyword in column_name for keyword in time_keyword)
        converted = pd.to_datetime(df[column], errors = "coerce")
        if is_datetime  :
            dict_1[column] = {"type" : "datetime",
                              "reason" : "Detected from datetim data"
            }
        elif is_keyword :
            dict_1[column] = {"type" : "time_column",
                              "reason" : "Detected from column name"}    
        elif converted.notna().mean() > 0.9 :
            dict_1[column] = {"type" : "date_string",
                              "reason" : "Most values can be converted to datetime"}
    return {
        "time_columns" : dict_1
    }    

def detect_price_columns(df) :
    dict_1 = {}
    for column in df.columns :
        column_name = column.lower().strip().replace("_"," ")
        for price_type, aliases in PRICE_ALIASES.items() :
            normalized_aliases = [alias.lower().strip().replace("_"," ") for alias in aliases]
            if column_name in normalized_aliases :
                dict_1[price_type] = column
                break
    return {
        "price_columns" : dict_1
    }

def detect_volume_columns(df) :
    dict_1 = {}
    for column in df.columns :
        column_name = column.lower().strip().replace("-"," ")
        for volume_type , aliases in VOLUME_ALIASES.items() :
            normalized_aliases =[alias.lower().strip().replace("_"," ") for alias in aliases]
            if column_name in normalized_aliases :
                dict_1[volume_type] = column
                break
    return {
        "volume_columns" : dict_1
    }        

def detect_target_columns(df) :
    for target_type, aliases in TARGET_PRIORITY.items() :
        for column in df.columns :
            column_name = column.lower().strip().replace("_"," ")
            normalized_aliases =[alias.lower().strip().replace("_"," ") for alias in aliases]
            if column_name in normalized_aliases :
                return{"target_columns" : {"column" : column,
                                          "type" : target_type,
                                         "confidence" : aliases["confidence"],
                                         "reason" : aliases["reason"]}
        }                
    return {
            "target_columns" : None,
            "type" : None,
            "confidence" : "Low",
            "reason" : "No suitable target column detected"        
            }        

def detect_market_columns(df):
    dict_1 = {}
    for column in df.columns :
        column_name = column.lower().strip().replace("_"," ")
        for market_type, aliases in MARKET_ALIASES.items() :
            normalized_aliases = [alias.lower().strip().replace("_"," ") for alias in aliases]
            if column_name in normalized_aliases :
                dict_1[market_type] = column
                break
    return {
        "market_columns" : dict_1
    }

def detect_constant_columns(df):
    dict_1 = {}
    for column in df.columns :
        series = df[column].dropna()
        if series.empty :
            continue
        if series.nunique() == 1:
            dict_1[column] = {"constant_value" : series.iloc[0],
                                  "reason" : "No variation detected in this column"}
    return {"constant_columns" : dict_1}            

def detect_high_cardinality_columns(df):
    dict_1 = {}
    cardinal_df = df.select_dtypes(include = ["object", "string", "category"])
    for column in cardinal_df.columns :
        series = df[column].dropna()
        if series.empty :
            continue
        if len(series) < MINIMUM_ROWS_FOR_CARDINALITY:
            continue
        unique_percentage = (series.nunique()/len(series))*100
        if unique_percentage >= HIGH_CARDINALITY_THRESHOLD :
            dict_1[column] = {"unique_count" : series.nunique(),
                              "unique_percentage" : round(unique_percentage,2),
                              "reason" : f"Unique values exceed {HIGH_CARDINALITY_THRESHOLD}% of non-null rows"}
    return {"high_cardinality_columns" : dict_1 }

def detect_text_columns(df):
    dict_1 = {}
    cardinal_df = df.select_dtypes(include = ["object", "string", "category"])
    for column in cardinal_df.columns :
        column_name = column.lower().strip().replace("_"," ")
        is_keyword = any(keyword in column_name for keyword in TEXT_KEYWORDS)
        series = df[column].dropna()
        if series.empty :
            continue
        average_length = series.astype(str).str.len().mean()
        if average_length > 50 or is_keyword :
            dict_1[column] = {"average_length" : average_length,
                              "reason" : "detected as free-form text"}
    return {"text_columns" : dict_1 }

def detect_boolean_columns(df):
    dict_1 = {}
    for column in df.columns :
        series = df[column].dropna()
        if series.empty:
            continue
        unique_values = set(series.astype(str).str.lower().str.strip().unique())
        if any(unique_values == alias for alias in BOOLEAN_ALIASES):
            dict_1[column] = {"values" : sorted(unique_values),
                              "unique_count" : len(unique_values),
                              "reason" : "Column contains binary categorical values"}
    return {"boolean_columns" : dict_1}        

def generate_financial_recommendations(profile):
    recommendations = []
    # Missing Values
    missing = profile["missing_values"]["missing values"]
    if missing :
        recommendations.append({"priority" : "Critical",
                                "category" : "Data Quality",
                                "message" : "Missing values detected.Consider imputing or removing them."})
    # Duplicate Values
    duplicates = profile["duplicate_count"]["Duplicate Rows"]
    if duplicates > 0:
        recommendations.append({"priority" : "warning",
                                "category" : "Data Quality",
                                "message" : f"{duplicates} duplicate rows detected."})
    # constant Values
    constants = profile["constant_columns"]["constant_columns"]
    if constants :
        recommendations.append({"priority" : "warning",
                                "category" : "Feature Engineering",
                                "message" : "Constant columns detected. They provide no predictive value "})
        
    # High Cardinality
    high_cardinality = profile["high_cardinality_columns"]["high_cardinality_columns"]
    if high_cardinality :
        recommendations.append({"priority" : "Medium",
                                "category" : "Feature Engineering",
                                "message" : "High-cardinality categorical columns detected. Consider target/fequency encoding."})
    # Outliers
    outliers = profile["detect_outliers"]["outlier"]
    if outliers :
        recommendations.append({"priority" : "Medium",
                                "category" : "Data Quality",
                                "message" : "Outliers detected. Review them before model training"
        })
    # Data quality score
    quality = profile["data_quality_score"]["quality_score"]
    if quality < 70 :
        recommendations.append({"priority" : "critical",
                                "category" : "Data Quality",
                                "message" : f"Dataset quality score is only {quality}%. Clean the dataset before modelling."
        })
    # Volume Columns
    volume_columns = profile["volume_columns"]["volume_columns"]
    if not volume_columns :
        recommendations.append({"priority" : "Info",
                                "category" : "Finance",
                                "message" : "No volume column detected"
        })    
    # Target Column
    target = profile["target_columns"].get("target_columns")
    if target is None :
        recommendations.append({"priority" : "Info",
                                "category" : "Machine Learning",
                                "message" : "No target column detected. Supervised learning cannot be performed."
        })
    elif target.get("column") is None :
           recommendations.append({"priority" : "Info",
                                   "category" : "Machine Learning",
                                   "message" : "No target column detected. Supervised learning cannot be performed."
        })
    else : 
        recommendations.append({"priority" : "Success",
                                "category" : "Machine Learning",
                                "message" : f"Target column selected : {target['column']}"
        })       
    # Time column
    time_columns = profile["time_columns"]["time_columns"]
    if not time_columns :
        recommendations.append({"priority" : "Warning",
                                "category" : "Time series",
                                "message" : "No time column detected. Time-series analysis may not be possible."
        })
    # Price column
    price_columns = profile["price_columns"]["price_columns"]
    if not price_columns :
        recommendations.append({"priority" : "Warning",
                                "category" : "Finance",
                                "message" : "No price column detected."
        })
    # High correlated features
    # Boolean columns
    boolean_columns = profile["boolean_columns"]["boolean_columns"]
    if boolean_columns :
        recommendations.append({"priority" : "Info",
                                "category" : "Feature Engg",
                                "message" : "Boolean columns detected. Verify they are encoded correctly."
        })
    # Text Columns
    text_columns = profile["text_columns"]["text_columns"]
    if text_columns :
        recommendations.append({"priority" : "Info",
                                "category" : "NLP",
                                "message" : "Free-text columns detected. Apply text preprocessing or embeddings if needed"
        })
    # Market columns 
    market_columns = profile["market_columns"]["market_columns"]
    if market_columns :
        recommendations.append({"priority" : "Info",
                                "category" : "Finance",
                                "message" : "Market-related columns detected. These may improve predictive performance."
        })

    return {"financial_recommendations" : recommendations}            

def generate_profile(df):
  try :
        profile = {
        "dataset_summary" : get_dataset_summary(df),
        "missing_values" : get_missing_values(df),
        "duplicate_count" : get_duplicate_count(df),
        "data_types" : get_data_types(df),
        "basic_statistics" : get_basic_statistics(df),
        "numeric_columns" : get_numeric_columns(df),
        "categorical_columns" : get_categorical_columns(df),
        "unique_values" : get_unique_values(df),
        "corrlation_matrix" : get_correlation_matrix(df),
        "detect_outliers" : detect_outliers(df),
        "data_quality_score" : get_data_quality_score(df),
        "diastribution_analysis" : get_distribution_analysis(df),
        "time_columns" : detect_time_column(df),
        "price_columns" : detect_price_columns(df),
        "volume_columns" : detect_volume_columns(df),
        "target_columns" : detect_target_columns(df),
        "market_columns" : detect_market_columns(df),
        "constant_columns" : detect_constant_columns(df),
        "high_cardinality_columns" : detect_high_cardinality_columns(df),
        "text_columns" : detect_text_columns(df),
        "boolean_columns" : detect_boolean_columns(df),
        }
        profile["financial_recommendations"] = generate_financial_recommendations(profile)
        return profile
except Exception as e:
        print("PROFILE ERROR : ",e)
        raise

