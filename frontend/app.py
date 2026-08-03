import os
import time
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

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
TWELVE_DATA_API_KEY = "47962a3fa52846e39013254eb698cb1c"
st.header("Download Stock Dataset")

ticker = st.text_input(
    "Enter NSE Symbol",
    "RELIANCE.NSE"
)

if st.button("Download Data"):

    with st.spinner("Downloading data from Twelve Data..."):

        url = (
            "https://api.twelvedata.com/time_series"
            f"?symbol={ticker}"
            "&interval=1day"
            "&outputsize=5000"
            f"&apikey={TWELVE_DATA_API_KEY}"
        )

        try:
            response = requests.get(url, timeout=60)
            data = response.json()

            if "values" not in data:
                st.error(data.get("message", "Unable to download data."))
                st.stop()

            df = pd.DataFrame(data["values"])

            # Rename columns
            df.rename(columns={
                "datetime": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume"
            }, inplace=True)

            # Convert datatypes
            df["Date"] = pd.to_datetime(df["Date"])

            numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            # Sort oldest -> newest
            df.sort_values("Date", inplace=True)
            df.reset_index(drop=True, inplace=True)

            # Save CSV
            Path("data").mkdir(exist_ok=True)

            file_path = Path("data") / f"{ticker.replace('.', '_')}_5y.csv"

            df.to_csv(file_path, index=False)

            st.session_state["dataset_path"] = str(file_path)

            st.success(f"Saved to {file_path}")

            st.dataframe(df.head())

            # Upload to backend
            with open(file_path, "rb") as f:

                upload_response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={"file": f},
                    timeout=90
                )

            if upload_response.status_code == 200:

                st.success("Dataset uploaded successfully!")

                profile_response = requests.get(
                    f"{BACKEND_URL}/profile",
                    timeout=120
                )

                if profile_response.status_code == 200:
                    st.success("Profile generated successfully.")
                else:
                    st.warning(profile_response.text)

            else:
                st.error(upload_response.text)

        except Exception as e:
            st.error(f"Error: {e}")
