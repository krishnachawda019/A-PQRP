import yfinance as yf
df = yf.download("RELIANCE.NS", period = "5y", auto_adjust = False, progress = False)
# Remove multi-index columns if present
if hasattr(df.columns, "droplevel"):
    try :
        df.columns = df.columns.droplevel(1)
    except :
        pass
df.reset_index(inplace = True)        
df.to_csv("reliance_5y.csv",)
print(df.head())
print("Dataset downloaded successfuly!")