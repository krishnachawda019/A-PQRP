import streamlit as st 

def show_sidebar() :
    if st.session_state.get("logged_in", False) :
        st.sidebar.success(f"Logged in as {st.session_state['user_email']}")
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout") :
            st.session_state.clear()
            st.switch_page("pages/00_Login.py")