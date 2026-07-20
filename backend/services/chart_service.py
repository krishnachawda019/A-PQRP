import pandas as pd 
import ta

def add_indicators(df):
    df["SMA20"] = ta.trend.sma_indicator(df["Colse"], window = 20)
    df["SMA50"] = ta.trend.sma_indicator(df["Close"], window = 50)
    df["EMA20"] = ta.trend.ema_indicator(df["Close"], window = 20)
    df["RSI"] = ta.momentum.rsi(df["Close"], window = 14)
    macd = ta.momentum.rsi(df["Close"])
    df["MACD"] = macd.macd()
    df["Signal"] = macd.macd_signal()
    bb = ta.volatility.BollingerBands(df["Close"])
    df["UpperBand"] = bb.bollinger_hband()
    df["LowerBand"] = bb.bollinger_lband()
    return df