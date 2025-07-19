import streamlit as st
import json
import os
from datetime import datetime

MEETINGS_FILE = "data/scheduled_meetings.json"

def load_meetings():
    if os.path.exists(MEETINGS_FILE):
        with open(MEETINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_meeting(meeting):
    meetings = load_meetings()
    meetings.append(meeting)
    with open(MEETINGS_FILE, "w") as f:
        json.dump(meetings, f, indent=2)

# UI
st.title("📅 Schedule a Meeting")

employee = st.session_state["employee"]
room_name = f"{employee['department']}_{employee['name'].replace(' ', '')}"
video_link = f"https://meet.jit.si/{room_name}"

with st.form("ScheduleMeeting"):
    topic = st.text_input("Meeting Topic")
    date = st.date_input("Date")
    time = st.time_input("Time")
    agenda = st.text_area("Agenda")
    submitted = st.form_submit_button("Schedule")

    if submitted:
        meeting = {
            "host": employee["name"],
            "department": employee["department"],
            "topic": topic,
            "datetime": f"{date} {time}",
            "agenda": agenda,
            "link": video_link
        }
        save_meeting(meeting)
        st.success("✅ Meeting scheduled!")
        st.markdown(f"🔗 [Join Meeting]({video_link})")

st.markdown("---")
st.subheader("📋 Upcoming Meetings")

for m in load_meetings():
    st.markdown(f"**{m['topic']}** — hosted by *{m['host']}*")
    st.caption(f"🕒 {m['datetime']}")
    st.markdown(f"📝 {m['agenda']}")
    st.markdown(f"[🔗 Join Meeting]({m['link']})")
    st.markdown("---")
