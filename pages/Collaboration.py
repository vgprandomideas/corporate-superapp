import streamlit as st
import os
import json
from datetime import datetime, timedelta

# --- Setup ---
CHAT_FILE = "data/chat.json"
MEETINGS_FILE = "data/scheduled_meetings.json"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Mock Login State ---
employee = st.session_state.get("employee", {
    "name": "Guruprasad",
    "department": "Engineering",
    "role": "Executive"
})
user_name = employee["name"]
user_dept = employee["department"]

# --- Helpers ---
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

chat_data = load_json(CHAT_FILE)
meetings = load_json(MEETINGS_FILE)

# --- UI Setup ---
st.set_page_config(page_title="Collaboration", layout="wide")
st.title("🤝 Unified Collaboration Space")
st.caption(f"Welcome **{user_name}** from `{user_dept}`")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📅 Schedule", "⏳ Meetings"])

# ------------------------ CHAT TAB ------------------------
with tab1:
    st.subheader("💬 Department Chat")
    msg = st.text_input("Message")
    file = st.file_uploader("Attach File", type=["pdf", "jpg", "png", "mp4", "zip", "docx"])

    if st.button("Send Message", use_container_width=True):
        file_path = None
        if file:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
        if msg.strip():
            chat_data.append({
                "room": user_dept,
                "sender": user_name,
                "message": msg,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "file": file_path,
                "replies": []
            })
            save_json(chat_data, CHAT_FILE)
            st.success("Message sent!")
            st.experimental_rerun()

    st.markdown("---")
    for i, entry in enumerate(reversed(chat_data[-20:])):
        if entry["room"] != user_dept:
            continue
        with st.container():
            st.markdown(f"**{entry['sender']}** _({entry['timestamp']})_")
            st.markdown(entry['message'])
            if entry.get("file"):
                st.markdown(f"[📎 File]({entry['file']})")
            for r in entry["replies"]:
                st.markdown(f"↪️ {r['sender']} replied: {r['message']}")

# ------------------------ SCHEDULE TAB ------------------------
with tab2:
    st.subheader("📅 Schedule a New Meeting")
    try:
        with open("data/employees.json", "r") as f:
            employees = json.load(f)
    except:
        employees = []

    names = [e["name"] for e in employees if e["name"] != user_name]
    participants = st.multiselect("👥 Select Participants", names)
    title = st.text_input("Meeting Title")
    description = st.text_area("Description")
    date = st.date_input("Date")
    hour = st.slider("Hour", 0, 23, 10)
    minute = st.slider("Minute", 0, 59, 0)
    full_datetime = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)

    if st.button("📌 Schedule", use_container_width=True):
        if not participants or not title:
            st.warning("Please fill all required fields.")
        else:
            new_meeting = {
                "title": title,
                "description": description,
                "organizer": user_name,
                "participants": participants,
                "time": full_datetime.strftime("%Y-%m-%d %H:%M")
            }
            meetings.append(new_meeting)
            save_json(meetings, MEETINGS_FILE)
            st.success("✅ Meeting Scheduled!")

# ------------------------ MEETINGS TAB ------------------------
with tab3:
    st.subheader("⏳ Upcoming Meetings")
    if not meetings:
        st.info("No upcoming meetings.")
    else:
        for m in sorted(meetings, key=lambda x: x["time"]):
            with st.expander(f"📌 {m['title']} on {m['time']}"):
                st.markdown(f"👤 Organizer: **{m['organizer']}**")
                st.markdown(f"👥 Participants: {', '.join(m['participants'])}")
                st.markdown(f"📝 {m['description']}")
