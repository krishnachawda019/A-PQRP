import time
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
import yfinance as yf

from components.sidebar import show_sidebar
from config.settings import BACKEND_URL

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="A-PQRP",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

show_sidebar()

# ---------------------- CSS ----------------------
css_file = Path(__file__).parent / "assets" / "style.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text()}</style>", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
col1, col2 = st.columns([1, 6])

with col1:
    logo = Path("assets/A-PQRP_logo.png")
    if logo.exists():
        st.image(str(logo), width=80)

with col2:
    st.title("AI Powered Quant Research Platform")
    st.caption(
        "Financial Dataset Profiling • Market Analysis • ML Prediction"
    )

st.divider()

def upload_dataset(uploaded_file):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = None

    with st.spinner("Uploading dataset..."):

        for _ in range(6):

            try:
                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=90
                )

                if response.status_code == 200:
                    break

            except requests.exceptions.RequestException:
                time.sleep(5)

    return response

def generate_profile():

    response = requests.get(
        f"{BACKEND_URL}/profile",
        timeout=120
    )

    if response.status_code == 200:
        st.success("✅ Dataset profile generated.")

    else:
        st.warning(response.text)

def download_stock(ticker):

    Path("data").mkdir(exist_ok=True)

    csv_path = Path("data") / f"{ticker.replace('.', '_')}_5y.csv"

    if csv_path.exists():

        st.success("Loaded from local storage.")

        return pd.read_csv(csv_path)

    with st.spinner("Downloading stock data..."):

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            progress=False,
            auto_adjust=False,
            threads=False
        )

    if df.empty:
        st.error("No data found.")
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)

    df.to_csv(csv_path, index=False)

    return df

st.header("Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:

    response = upload_dataset(uploaded_file)

    if response is None:
        st.error("Backend unavailable.")
        st.stop()

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    result = response.json()

    st.session_state["dataset_path"] = result["dataset_path"]

    st.success("Dataset uploaded successfully!")

    generate_profile()

st.header("Download Stock Dataset")

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

ticker = st.selectbox(
    "Select Stock",
    stocks
)

if st.button("Download Data"):

    df = download_stock(ticker)

    if df is not None:

        st.session_state["dataset_path"] = (
            f"data/{ticker.replace('.', '_')}_5y.csv"
        )
        st.session_state["stock_symbol"] = ticker

        st.success("Dataset Ready")

        st.write(f"Rows : {len(df)}")
        st.dataframe(df.head())

        # Upload downloaded dataset to backend
        from io import BytesIO

        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        files = {
            "file": (
                f"{ticker.replace('.', '_')}_5y.csv",
                csv_buffer.getvalue(),
                "text/csv"
            )
        }

        upload_response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=90
        )

        if upload_response.status_code == 200:
            st.success("Dataset uploaded to backend successfully.")
        else:
            st.error(upload_response.text)
