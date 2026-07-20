import streamlit as st    
from auth_guard import check_login
from components.sidebar import show_sidebar

show_sidebar()
check_login()

st.title("👤 User Profile")
st.write("ACCOUNT INFORMATON")
st.write("USER NAME : ", st.session_state.get("user_name", "Not Available"))
st.write("Email : ", st.session_state.get("user_email"))