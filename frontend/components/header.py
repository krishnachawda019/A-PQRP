import streamlit as st 

def show_header() :
    st.set_page_config(
        page_title = "A-PQRP",
        page_icon = "📈",
        layout = "wide"
    )

    st.title("📈 AI-Powered Quant Research Platform")
    st.caption("Analyze . Backtest . Predict . Generate . AI Insights")
    