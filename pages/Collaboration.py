import os
import json
from datetime import datetime
import streamlit as st
import streamlit as st
from utils.auth import login_user

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    login_user()
    st.stop()


# ---------- File Path ----------
CHAT_FILE = "data/chat.json"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Utilities ----------
def load_chat():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_chat(data):
    with open(CHAT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_message(room, sender, message, file_url=None):
    chat = load_chat()
    chat.append({
        "room": room,
        "sender": sender,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file": file_url,
        "replies": []
    })
    save_chat(chat)

def add_reply(parent_index, sender, reply):
    chat = load_chat()
    if 0 <= parent_index < len(chat):
        chat[parent_index]["replies"].append({
            "sender": sender,
            "message": reply,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    save_chat(chat)

# ---------- UI Begins ----------
st.title("💬 Team Collaboration Space")
employee = st.session_state["employee"]
user_name = employee["name"]
user_dept = employee["department"]
role = employee["role"]
rooms = ["General", "Engineering", "Marketing", "Ops", "HR", "Finance", "Design"]
room = st.sidebar.selectbox("📁 Select Room", rooms, index=rooms.index(user_dept) if user_dept in rooms else 0)

st.markdown(f"**Welcome {user_name}! You are in `{room}` Room.**")
st.divider()

# ---------- New Message ----------
with st.expander("➕ New Message"):
    msg = st.text_area("Type your message:")
    uploaded_file = st.file_uploader("Attach a file (optional)", type=["jpg", "png", "pdf", "docx", "mp4", "zip"])
    if st.button("Send"):
        file_url = None
        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            file_url = f"{UPLOAD_DIR}/{uploaded_file.name}"
        if msg.strip() != "":
            add_message(room, user_name, msg, file_url)
            st.success("Message sent.")
            st.rerun()

# ---------- Display Messages ----------
chat_data = load_chat()
for idx, entry in enumerate(reversed(chat_data)):
    if entry["room"] != room:
        continue

    st.markdown(f"**{entry['sender']}** _({entry['timestamp']})_")
    st.markdown(entry["message"])
    if entry.get("file"):
        st.markdown(f"[📎 Attached File]({entry['file']})")

    # Reply Expander
    with st.expander("💬 Replies"):
        for r in entry["replies"]:
            st.markdown(f"➡️ **{r['sender']}** _({r['timestamp']})_: {r['message']}")
        with st.form(f"reply_form_{idx}"):
            reply_text = st.text_input("Your reply")
            submitted = st.form_submit_button("Reply")
            if submitted and reply_text.strip():
                add_reply(len(chat_data) - 1 - idx, user_name, reply_text)
                st.success("Reply added.")
                st.rerun()
# ------------------- SCHEDULED MEETING SECTION -------------------
import json
from datetime import datetime, timedelta

st.markdown("### 📅 Schedule a Meeting")

# Load employees
with open("data/employees.json", "r") as f:
    employees = json.load(f)

employee_names = [emp["name"] for emp in employees if emp["name"] != employee["name"]]
selected_participants = st.multiselect("👥 Select Participants", employee_names)
meeting_title = st.text_input("📝 Meeting Title")
meeting_description = st.text_area("🧾 Description")
meeting_datetime = st.datetime_input("📅 Date & Time", value=datetime.now() + timedelta(hours=1))

if st.button("📌 Schedule Meeting"):
    if not (selected_participants and meeting_title):
        st.warning("Please fill in all required fields.")
    else:
        meeting = {
            "title": meeting_title,
            "description": meeting_description,
            "organizer": employee["name"],
            "participants": selected_participants,
            "time": meeting_datetime.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open("data/scheduled_meetings.json", "r") as f:
                meetings = json.load(f)
        except:
            meetings = []

        meetings.append(meeting)

        with open("data/scheduled_meetings.json", "w") as f:
            json.dump(meetings, f, indent=2)

        st.success("✅ Meeting Scheduled!")

# ------------------- UPCOMING MEETINGS -------------------
st.markdown("### ⏳ Upcoming Meetings")

try:
    with open("data/scheduled_meetings.json", "r") as f:
        meetings = json.load(f)
except:
    meetings = []

if meetings:
    for mtg in sorted(meetings, key=lambda x: x["time"]):
        st.markdown(f"**{mtg['title']}**")
        st.markdown(f"🕒 {mtg['time']}")
        st.markdown(f"👤 Organizer: {mtg['organizer']}")
        st.markdown(f"👥 Participants: {', '.join(mtg['participants'])}")
        st.markdown(f"📝 {mtg['description']}")
        st.markdown("---")
else:
    st.info("No meetings scheduled.")
