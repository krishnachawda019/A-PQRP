import streamlit as st     
import pandas as pd  
import plotly.graph_objects as go 
import ta
from pathlib import Path       
from plotly.subplots import make_subplots
from components.sidebar import show_sidebar

show_sidebar()

st.title("📈 Market Analysis")
if "dataset_path" not in st.session_state :
    st.warning("Please download a dataset first")
    st.stop()
csv_path = Path(st.session_state["dataset_path"])
df = pd.read_csv(csv_path)    

fig = make_subplots(rows = 4,
                    cols = 1,
                    shared_xaxes = True,
                    vertical_spacing = 0.03,
                    row_heights = [0.50, 0.15, 0.15, 0.20],
                    subplot_titles = ("Price", "Volume", "RSI", "MACD"))

fig.add_trace(
    go.Candlestick(x = df["Date"],
                   open = df["Open"],
                   high = df["High"],
                   low = df["Low"],
                   close = df["Close"],
                   name = "Price"),
    row = 1,
    col = 1
)

fig.add_trace(
    go.Bar(x = df["Date"],
           y = df["Volume"],
           name = "Volume",
           marker_color = "deepskyblue"),
    row = 2,
    col = 1       
)

df["Close"] = pd.to_numeric(df["Close"], errors = "coerce")
df["Open"] = pd.to_numeric(df["Open"], errors = "coerce")
df["High"] = pd.to_numeric(df["High"], errors = "coerce")
df["Low"] = pd.to_numeric(df["Low"], errors = "coerce") 

# Simple Moving Averages
df["SMA20"] = ta.trend.sma_indicator(df["Close"], window = 20)
df["SMA50"] = ta.trend.sma_indicator(df["Close"], window = 50)

# Exponential Moving Averages
df["EMA20"] = ta.trend.ema_indicator(df["Close"], window = 20)

# Relative Strength Index
df["RSI"] = ta.momentum.rsi(df["Close"], window = 14)

# Moving Average Convergence Divergence
macd = ta.trend.MACD(df["Close"])
df["MACD"] = macd.macd()
df["MACD_SIGNAL"] = macd.macd_signal()

# Bollinger Bands
bb = ta.volatility.BollingerBands(df["Close"], window = 20)
df["BB_UPPER"] = bb.bollinger_hband()
df["BB_LOWER"] = bb.bollinger_lband()

st.sidebar.header("Technical Indicators")
show_sma20 = st.sidebar.checkbox("SMA 20")
show_sma50 = st.sidebar.checkbox("SMA 50")
show_ema20 = st.sidebar.checkbox("EMA 20")
show_bb = st.sidebar.checkbox("Bollinger Bands")

fig.add_trace(go.Scatter(x = df["Date"],
                         y = df["Close"],
                         name = "Close"))

if show_sma20 :
    fig.add_trace(go.Scatter(x = df["Date"],
                             y = df["SMA20"],
                             name = "SMA 20",
                             line = dict(color = "orange")
                             ),
                            row = 1,
                            col = 1           
                )

if show_sma50 :
    fig.add_trace(go.Scatter(x = df["Date"],
                             y = df["SMA50"],
                             name = "SMA 50",
                             line = dict(color = "blue")
                             ),
                            row = 1,
                            col = 1           
                )      
    
if show_ema20 :
    fig.add_trace(go.Scatter(x = df["Date"],
                             y = df["EMA20"],
                             name = "EMA 20",
                             line = dict(color = "green")
                             ),
                            row = 1,
                            col = 1           
                )    
if show_bb :
    fig.add_trace(go.Scatter(x = df["Date"],
                             y = df["BB_UPPER"],
                             name = "BB Upper",
                             line = dict(color = "gray", dash = "dot")
                             ),
                            row = 1,
                            col = 1           
                )    
    fig.add_trace(go.Scatter(x = df["Date"],
                             y = df["BB_LOWER"],
                             name = "BB Lower",
                             line = dict(color = "gray", dash = "dot")
                             ),
                            row = 1,
                            col = 1           
                )   

fig.add_trace(go.Scatter(x = df["Date"],
                         y = df["RSI"],
                         name = "RSI",
                         line = dict(color = "purple")
                         ),
                         row = 3,
                         col = 1
            )

fig.add_hline(y = 70,
              line_dash = "dash",
              line_color = "red",
              row = 3,
              col = 1
              )

fig.add_hline(y = 30,
              line_dash = "dash",
              line_color = "green",
              row = 3,
              col = 1
              )

fig.add_trace(go.Scatter(x = df["Date"],
                         y = df["MACD"],
                         name = "MACD",
                         line = dict(color = "orange")
                         ),
                         row = 4,
                         col = 1
              )

fig.add_trace(go.Scatter(x = df["Date"],
                         y = df["MACD_SIGNAL"],
                         name = "Signal",
                         line = dict(color = "blue")
                         ),
                         row = 4,
                         col = 1
              )

df["MACD_HISTOGRAM"] = df["MACD"] - df["MACD_SIGNAL"]

fig.add_trace(go.Bar(x = df["Date"],
                     y = df["MACD_HISTOGRAM"],
                     name = "Histogram"
                     ),
                     row = 4,
                     col = 1
             )

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    height=1100,
    xaxis_rangeslider_visible=False,
    legend_orientation="h"
)

st.plotly_chart(fig, use_container_width=True)