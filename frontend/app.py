import os
import time
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

import yfinance as yf
from components.sidebar import show_sidebar
from config.settings import BACKEND_URL

# PAGE CONFIG 
st.set_page_config(
    page_title="A-PQRP",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIDEBAR 
show_sidebar()

# LOAD CSS 
css_file = Path(__file__).parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HEADER 
col1, col2 = st.columns([1, 6])

with col1:
    logo = Path(__file__).parent / "assets" / "A-PQRP_logo.png"
    if logo.exists():
        st.image(str(logo), width=80)

with col2:
    st.title("AI Powered Quant Research Platform")
    st.caption("Financial Dataset Profiling • Market Analysis • ML Prediction")

st.divider()

# DATASET UPLOAD 
st.header("Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    upload_response = None

    with st.spinner("Uploading dataset..."):

        for attempt in range(6):

            try:
                upload_response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=90
                )

                if upload_response.status_code == 200:
                    break

            except requests.exceptions.RequestException:

                if attempt < 5:
                    st.info("Backend is starting... Please wait.")
                    time.sleep(5)

    if upload_response is None:
        st.error("Unable to connect to backend.")
        st.stop()

    if upload_response.status_code != 200:
        st.error(upload_response.text)
        st.stop()

    upload_result = upload_response.json()

    st.session_state["dataset_path"] = upload_result["dataset_path"]

    st.success("✅ Dataset uploaded successfully!")
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

ticker = st.selectbox("Select Stock", stocks)
# Generate profile
profile_response = requests.get(
    f"{BACKEND_URL}/profile",
    timeout=120
)

if profile_response.status_code == 200:
    st.success("✅ Dataset profile generated.")
else:
    st.warning(profile_response.text)

# DOWNLOAD STOCK DATA 


ticker = st.text_input("Enter NSE Symbol", "RELIANCE.NS")

if st.button("Download Data"):

    Path("data").mkdir(exist_ok=True)

    csv_path = Path("data") / f"{ticker.replace('.', '_')}_5y.csv"

    # CSV already exists
    if csv_path.exists():

        st.success("Dataset loaded from local storage.")

        df = pd.read_csv(csv_path)

        st.write(f"Rows: {len(df)}")

        st.dataframe(df.head())

    else:

        try:

            with st.spinner("Downloading from Yahoo Finance..."):

                df = yf.download(
                    ticker,
                    period="5y",
                    interval="1d",
                    auto_adjust=False,
                    progress=False,
                    threads=False
                )

            if df.empty:
                st.error("No data found.")
                st.stop()

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.reset_index(inplace=True)

            df.to_csv(csv_path, index=False)

            st.success("Dataset downloaded and saved.")

            st.dataframe(df.head())

        except Exception as e:

            st.error(f"Download failed: {e}")

            if csv_path.exists():

                st.info("Using previously saved dataset.")

                df = pd.read_csv(csv_path)

                st.dataframe(df.head())
