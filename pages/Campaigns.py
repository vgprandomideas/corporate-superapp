import streamlit as st
from utils.data import load_data, save_data, add_post

st.title("📢 Campaign Center")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view campaigns.")
    st.stop()

# Display campaigns
posts = load_data("posts.json")
campaigns = [post for post in reversed(posts) if "campaign" in post.get("tags", [])]

if campaigns:
    st.subheader("Active Campaigns")
    for post in campaigns:
        with st.expander("🎯 " + post["title"]):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Campaign started on " + post["timestamp"][:10])
            st.caption("Campaign by " + post["author"])
else:
    st.info("No active campaigns. Create one to get started!")

# Campaign creation form
st.subheader("Create New Campaign")
with st.form("CampaignForm"):
    title = st.text_input("Campaign Title")
    content = st.text_area("Campaign Message")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    
    if st.form_submit_button("Publish Campaign"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "All", 
                    ["campaign", priority.lower()])
            st.success("Campaign published successfully!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")