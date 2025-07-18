import streamlit as st
import json
import os
from datetime import datetime

FEEDBACK_FILE = "data/anonymous_feedback.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return []

def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

feedback_list = load_feedback()
employee = st.session_state["employee"]
is_admin = employee["role"] == "Admin"

st.title("🔒 Anonymous Feedback Portal")

# Anonymous Submission
with st.expander("✍️ Submit Anonymous Feedback"):
    message = st.text_area("Your Message (anonymous)")
    route_to = st.selectbox("Route To", ["Department Head", "Specific Person", "C-Suite", "Admin"])
    if st.button("Send Anonymously"):
        feedback = {
            "message": message,
            "route_to": route_to,
            "timestamp": datetime.now().isoformat()
        }
        feedback_list.append(feedback)
        save_feedback(feedback_list)
        st.success("Feedback sent anonymously.")

# Admin View
if is_admin:
    st.subheader("📬 Anonymous Feedback Received")
    for fb in feedback_list:
        with st.container():
            st.markdown(f"**To:** {fb['route_to']}  \n**Submitted:** {fb['timestamp']}")
            st.write(fb["message"])
