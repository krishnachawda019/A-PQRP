import streamlit as st 

def show_sidebar():
    page = st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose Module",
        [
            "Dashboard",
            "Backtesting",
            "Analytics",
            "ML Prediction",
            "AI Report"
        ]
    )
    return page
