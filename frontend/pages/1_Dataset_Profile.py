import streamlit as st
import requests

from components.sidebar import show_sidebar
from config.settings import BACKEND_URL
show_sidebar()

st.title("📋 Dataset Profile")

try:
    profile_response = requests.get(f"{BACKEND_URL}/profile")
    profile_response.raise_for_status()
    response = profile_response.json()
    if response.get("status") == "success":
        profile = response["profile"]
    else :
        st.error(response.get("message", "Unknown error"))
        st.stop()
except Exception as e:
    st.error(f"Unable to load profile: {e}")
    st.stop()

# Dataset Summary
st.header("📊 Dataset Summary")
summary = profile["dataset_summary"]
c1, c2, c3 = st.columns(3)
c1.metric("Rows", summary["Rows"])
c2.metric("Columns", summary["Columns"])
c3.metric("Memory Usage", f'{summary["Memory Usage"] / 1024:.2f}KB')

# Data Quality
st.header("✅ Data Quality")
quality_score = profile["data_quality_score"]["quality_score"]
st.metric("Quality Score", quality_score)
st.progress(min(int(quality_score), 100))

# Recommendations
st.header("💡 Recommendations")
rec_data = profile["financial_recommendations"]
if isinstance(rec_data, dict):
    recommendations = rec_data["financial_recommendations"]
else:
    recommendations = rec_data
for rec in recommendations:
    priority = rec["priority"]
    category = rec["category"]
    message = rec["message"]
    if priority == "Critical":
        st.error(f"🔴 {category}\n\n{message}")
    elif priority == "Medium":
        st.warning(f"🟡 {category}\n\n{message}")
    else:
        st.info(f"🔵 {category}\n\n{message}")
