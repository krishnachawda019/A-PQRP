import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)
from backend.models.ml_prediction import train_model
from components.sidebar import show_sidebar

show_sidebar()

st.title("📈 XGBoost Stock Prediction")

csv_path = st.session_state["dataset_path"]

df = pd.read_csv(csv_path)

(
    model,
    prediction,
    rmse,
    mae,
    r2,
    feature_names,
    X_train,
    X_test,
    y_train,
    y_test,
    df
) = train_model(df)

st.subheader("📊 Model Performance")

c1, c2, c3 = st.columns(3)

c1.metric("RMSE", f"{rmse:.2f}")
c2.metric("MAE", f"{mae:.2f}")
c3.metric("R² Score", f"{r2:.4f}")

st.divider()

importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

st.subheader("📌 Feature Importance")

st.bar_chart(
    importance.set_index("Feature")
)

st.divider()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=y_test,
        mode="lines",
        name="Actual"
    )
)

fig.add_trace(
    go.Scatter(
        y=prediction,
        mode="lines",
        name="Predicted"
    )
)

st.subheader("📉 Actual vs Predicted")

st.plotly_chart(fig, use_container_width=True)

st.divider()

latest = df[feature_names].iloc[[-1]]

tomorrow = model.predict(latest)[0]

st.subheader("🔮 Tomorrow Prediction")

st.success(f"Predicted Closing Price : ₹{tomorrow:.2f}")

future_days = 30

future_predictions = []

last = latest.copy()

for i in range(future_days):

    p = model.predict(last)[0]

    future_predictions.append(p)

    last["Open"] = p
    last["High"] = p
    last["Low"] = p

    last["EMA20"] = p
    last["SMA20"] = p
    last["SMA50"] = p

future_dates = pd.date_range(
    start=df["Date"].iloc[-1] + pd.Timedelta(days=1),
    periods=future_days
)

future_df = pd.DataFrame({
    "Date": future_dates,
    "Prediction": future_predictions
})

st.subheader("🗓 Next 5-Day Prediction")

st.dataframe(future_df.head())

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Close"],
        name="Historical"
    )
)

fig.add_trace(
    go.Scatter(
        x=future_df["Date"],
        y=future_df["Prediction"],
        name="Forecast"
    )
)

st.subheader("📈 30-Day Forecast")

st.plotly_chart(fig, use_container_width=True)

current_price = df["Close"].iloc[-1]

expected_return = (
    (future_predictions[-1] - current_price)
    / current_price
) * 100

confidence = max(
    0,
    min((r2 + 1) / 2 * 100, 100)
)

st.subheader("📊 Prediction Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current", f"₹{current_price:.2f}")
c2.metric("Tomorrow", f"₹{tomorrow:.2f}")
c3.metric("30 Days", f"₹{future_predictions[-1]:.2f}")
c4.metric("Expected Return", f"{expected_return:.2f}%")

st.metric("Prediction Confidence", f"{confidence:.1f}%")

st.progress(int(confidence))

volatility = df["Close"].pct_change().std() * 100

st.subheader("⚠ Risk Analysis")

if volatility < 1:
    st.success(f"Low Risk ({volatility:.2f}%)")
elif volatility < 2.5:
    st.warning(f"Medium Risk ({volatility:.2f}%)")
else:
    st.error(f"High Risk ({volatility:.2f}%)")

sma20 = df["Close"].rolling(20).mean().iloc[-1]
sma50 = df["Close"].rolling(50).mean().iloc[-1]

st.subheader("📈 Market Trend")

if sma20 > sma50:
    st.success("Bullish Trend")
else:
    st.error("Bearish Trend")

if expected_return >= 8:
    signal = "🟢 BUY"

elif expected_return >= 2:
    signal = "🟡 HOLD"

else:
    signal = "🔴 SELL"

st.subheader("🤖 AI Recommendation")

st.info(f"""
Current Price : ₹{current_price:.2f}

Tomorrow Prediction : ₹{tomorrow:.2f}

30-Day Prediction : ₹{future_predictions[-1]:.2f}

Expected Return : {expected_return:.2f}%

Recommendation : {signal}
""")

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/xgboost_model.pkl")

st.success("✅ XGBoost Model Saved Successfully")

st.session_state["current_price"] = current_price
st.session_state["expected_return"] = expected_return
st.session_state["confidence"] = confidence
st.session_state["recommendation"] = signal
st.session_state["future_predictions"] = future_predictions
