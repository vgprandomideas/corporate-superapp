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
    
    # Show user info
    st.sidebar.success("Logged in as " + employee_name + " (" + dept + ")")
    
    # Navigation
    st.sidebar.markdown("---")
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Home Feed", "📢 Campaigns", "🧩 " + dept + " Space", "📊 Dashboard"]
    )
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    # Load page content without debug messages
    if "Home Feed" in page:
        try:
            with open("pages/Home.py", "r", encoding="utf-8") as f:
                exec(f.read())
        except Exception as e:
            st.error(f"Error loading Home page: {e}")
    
    elif "Campaigns" in page:
        try:
            with open("pages/Campaigns.py", "r", encoding="utf-8") as f:
                exec(f.read())
        except Exception as e:
            st.error(f"Error loading Campaigns page: {e}")
    
    elif "Dashboard" in page:
        try:
            with open("pages/Dashboard.py", "r", encoding="utf-8") as f:
                exec(f.read())
        except Exception as e:
            st.error(f"Error loading Dashboard page: {e}")
    
    elif dept + " Space" in page:
        try:
            with open("pages/" + dept + ".py", "r", encoding="utf-8") as f:
                exec(f.read())
        except Exception as e:
            st.error(f"Error loading {dept} page: {e}")