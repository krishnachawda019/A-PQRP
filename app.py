import streamlit as st

from components.header import show_header
from components.sidebar import show_sidebar

show_header()
page = show_sidebar()
st.write(f"You selected :{page}")