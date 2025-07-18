import streamlit as st
import json
import os
from datetime import datetime

FEEDBACK_FILE = "data/feedback.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_feedback(feedback_list):
    try:
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedback_list, f, indent=2)
    except Exception as e:
        st.error(f"Error saving feedback: {e}")

st.title("🔒 Anonymous Feedback Box")
st.markdown("Your identity will not be recorded. Share concerns, suggestions, or ideas freely.")

route_options = ["HR", "Engineering", "Marketing", "Leadership", "General"]
route_to = st.selectbox("Route this feedback to:", route_options)
feedback_text = st.text_area("Your feedback (no login trace)")

if st.button("Submit Feedback"):
    if feedback_text.strip():
        feedback_list = load_feedback()
        feedback_list.append({
            "route_to": route_to,
            "text": feedback_text.strip(),
            "timestamp": datetime.now().isoformat()
        })
        save_feedback(feedback_list)
        st.success("✅ Feedback submitted anonymously.")
    else:
        st.warning("Please write something before submitting.")
