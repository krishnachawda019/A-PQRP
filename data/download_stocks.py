import yfinance as yf
from pathlib import Path

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "SBIN.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "LT.NS",
    "AXISBANK.NS",
    "BHARTIARTL.NS"
]

Path("data").mkdir(exist_ok=True)

for stock in stocks:

    print(f"Downloading {stock}")

    df = yf.download(
        stock,
        period="5y",
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        print(f"Couldn't download {stock}")
        continue

    df.reset_index(inplace=True)

    filename = f"data/{stock.replace('.', '_')}_5y.csv"

    df.to_csv(filename, index=False)

print("Done!")
