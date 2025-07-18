import streamlit as st
from utils.auth import login_user
import os

st.set_page_config(page_title="Corporate Superapp", layout="wide")

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login flow
if not st.session_state.logged_in:
    login_user()
    st.stop()  # Don't proceed unless logged in

# After login
dept = st.session_state["employee"]["department"]
employee_name = st.session_state["employee"]["name"]
role = st.session_state["employee"]["role"]

# Sidebar
st.sidebar.image("https://placehold.co/180x80?text=Company+Logo", width=180)  # Replaced broken Imgur image
st.sidebar.success(f"👋 {employee_name} ({dept}, {role})")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "📁 Navigate",
    ["🏠 Home Feed", "📢 Campaigns", f"🧩 {dept} Space", "📊 Dashboard", "✅ Tasks", "🔒 Anonymous Feedback"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# Page Loader
page_map = {
    "🏠 Home Feed": "pages/Home.py",
    "📢 Campaigns": "pages/Campaigns.py",
    "📊 Dashboard": "pages/Dashboard.py",
    "✅ Tasks": "pages/Tasks.py",
    "🔒 Anonymous Feedback": "pages/Anonymous.py",
    f"🧩 {dept} Space": f"pages/{dept}.py"
}

try:
    with open(page_map[page], "r", encoding="utf-8") as f:
        exec(f.read())
except Exception as e:
    st.error(f"❌ Error loading {page}: {e}")
