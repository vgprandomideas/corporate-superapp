import streamlit as st
import json
import os
from datetime import datetime

# Paths
CHAT_FILE = "data/chat.json"
ROOM_FILE = "data/rooms.json"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper Functions
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Load session
employee = st.session_state.get("employee", {})
emp_name = employee.get("name")
emp_id = employee.get("id")

# Load rooms and chats
rooms = load_json(ROOM_FILE)
chat_data = load_json(CHAT_FILE)

# Sidebar: Room Selector
st.sidebar.subheader("📁 Chat Rooms")
accessible_rooms = [room for room in rooms if (room["type"] == "public" or emp_id in room["members"])]
room_names = [room["name"] for room in accessible_rooms]
selected_room = st.sidebar.selectbox("Select Room", room_names)

# New Room Creator
with st.sidebar.expander("➕ Create New Room"):
    new_room = st.text_input("Room Name")
    is_private = st.checkbox("Private Room?")
    allowed_ids = st.text_input("Allowed Employee IDs (comma-separated)", "")
    if st.button("Create Room"):
        room_obj = {
            "name": new_room,
            "type": "private" if is_private else "public",
            "members": [i.strip() for i in allowed_ids.split(",")] if is_private else []
        }
        rooms.append(room_obj)
        save_json(ROOM_FILE, rooms)
        st.success(f"Room '{new_room}' created.")
        st.experimental_rerun()

# Header
st.title(f"💬 Chat Room: {selected_room}")
st.markdown(f"Welcome {emp_name}! You're now chatting in **{selected_room}**.")

# Filter chat messages for room
room_msgs = [msg for msg in chat_data if msg["room"] == selected_room]

# Chat display
for msg in room_msgs:
    st.markdown(f"**{msg['sender']}** ({msg['timestamp']}): {msg['text']}")
    if msg.get("file_url"):
        st.markdown(f"[📎 Attached File]({msg['file_url']})")

# Chat input
with st.form("chat_form", clear_on_submit=True):
    msg = st.text_input("Type your message")
    uploaded_file = st.file_uploader("Attach file (optional)", type=["png", "jpg", "pdf", "mp4"])
    if st.form_submit_button("Send"):
        file_url = ""
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            file_url = f"./{UPLOAD_FOLDER}/{uploaded_file.name}"

        chat_data.append({
            "room": selected_room,
            "sender": emp_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": msg,
            "file_url": file_url
        })
        save_json(CHAT_FILE, chat_data)
        st.experimental_rerun()
