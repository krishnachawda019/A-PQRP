import streamlit as st   

# Login Check
def check_login() :
    if "logged_in" not in st.session_state :
        st.switch_page("pages/00_Login.py")