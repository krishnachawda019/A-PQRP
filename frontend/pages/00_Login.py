import streamlit as st  
import sys
from pathlib import Path
from components.sidebar import show_sidebar

show_sidebar()
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from backend.auth import login_user

st.set_page_config(page_title = "Login", page_icon = "🔐")
st.title("🔐 Login to A-PQRP")
email = st.text_input("Email")
password = st.text_input("Password", type = "password")

if st.button("Login") :
    user = login_user(email, password)
    if user :
        st.session_state["logged_in"] = True
        st.session_state["user_name"] = user[0]
        st.session_state["user_email"] = user[1]
        st.success("Logged in Successfully") 
        st.switch_page("app.py")
    else :
        st.error("Invalid Email or Password!")