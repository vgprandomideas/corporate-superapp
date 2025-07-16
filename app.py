import streamlit as st
from utils.auth import login_user

st.set_page_config(page_title="Corporate Superapp", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_user()
else:
    dept = st.session_state["employee"]["department"]
    employee_name = st.session_state["employee"]["name"]
    st.sidebar.success("Logged in as " + employee_name + " (" + dept + ")")
    st.sidebar.page_link("pages/Home.py", label="🏠 Home Feed")
    st.sidebar.page_link("pages/Campaigns.py", label="📢 Campaigns")
    st.sidebar.page_link("pages/" + dept + ".py", label="🧩 " + dept + " Space")
    st.sidebar.page_link("pages/Dashboard.py", label="📊 Dashboard")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()