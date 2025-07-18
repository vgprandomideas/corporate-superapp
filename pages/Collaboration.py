import streamlit as st
import os
import json
from datetime import datetime
import uuid

# Directories for chat & uploads
CHAT_FILE = "data/chat.json"
UPLOAD_FOLDER = "uploads"

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("🤝 Team Collaboration Hub")

# Logged-in user info
employee = st.session_state["employee"]
name = employee["name"]
department = employee["department"]

# --------- CHAT SECTION ---------
st.subheader("💬 Group Chat")

# Load chat
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        chat_data = json.load(f)
else:
    chat_data = []

# Display messages
for msg in reversed(chat_data[-50:]):
    st.markdown(f"**{msg['sender']}** *[{msg['timestamp']}]*")
    st.markdown(f"> {msg['text']}")

# New message input
msg = st.text_input("Type your message:")
if st.button("Send"):
    new_entry = {
        "id": str(uuid.uuid4()),
        "sender": name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "text": msg
    }
    chat_data.append(new_entry)
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=2)
    st.experimental_rerun()

st.markdown("---")

# --------- FILE UPLOAD ---------
st.subheader("📁 Share Files")

uploaded_file = st.file_uploader("Upload any document, image, or video")
if uploaded_file:
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"File uploaded: {filename}")

# Show uploaded files
st.markdown("### 🗂️ Uploaded Files")
for file in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(UPLOAD_FOLDER, file)
    if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        st.image(file_path, width=200)
    elif file.lower().endswith((".mp4", ".webm")):
        st.video(file_path)
    elif file.lower().endswith(".pdf"):
        st.markdown(f"[📄 {file}](/{file_path})")
    else:
        st.markdown(f"📎 {file}")

st.markdown("---")

# --------- VIDEO CALL BUTTON ---------
st.subheader("📹 Video Conference Room")

st.markdown("Click below to launch a secure meeting room.")
room_url = f"https://meet.jit.si/{department.replace(' ', '')}-{name}"
st.markdown(f"[🔗 Join Meeting Room]({room_url})", unsafe_allow_html=True)
