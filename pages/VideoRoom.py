import streamlit as st
import urllib.parse

st.title("📞 Video Conferencing Room")

employee = st.session_state["employee"]
room_name = f"{employee['department']}_{employee['name'].replace(' ', '')}"

st.markdown(f"Welcome to your secure video room, **{employee['name']}**.")
st.markdown("🔒 Each department-user pair gets a unique room.")

# Generate a Jitsi URL
base_url = "https://meet.jit.si"
jitsi_room = urllib.parse.quote(room_name)
iframe_url = f"{base_url}/{jitsi_room}"

# Embed video using iframe
st.markdown(
    f"""
    <iframe src="{iframe_url}#config.startWithAudioMuted=true&config.startWithVideoMuted=false"
            width="100%" height="700" allow="camera; microphone; fullscreen" style="border:0;">
    </iframe>
    """,
    unsafe_allow_html=True,
)
