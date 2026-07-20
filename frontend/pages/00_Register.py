import streamlit as st  
from backend.auth import register_user
from components.sidebar import show_sidebar

show_sidebar()
st.set_page_config(page_title = "Register", page_icon = "📝")
st.title("📝 Create Account")
name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type = "password")
confirm = st.text_input("Confirm Password", type = "password")

if st.button("Register") :
    if password != confirm :
        st.error("Password do not match!")
    elif register_user(name, email, password):
        st.success("Registration Successfull!")
        st.info("You can now login")
    else :
        st.error("Email already exists")        