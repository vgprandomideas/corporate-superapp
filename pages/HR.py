import streamlit as st
from utils.data import load_data, save_data, add_post

st.title("🧩 HR Department Feed")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the HR feed.")
    st.stop()

posts = load_data("posts.json")
dept_posts = [post for post in reversed(posts) if post["department"] == "HR"]

if dept_posts:
    st.subheader("HR Updates")
    for post in dept_posts:
        with st.expander(post["title"] + " - by " + post["author"]):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
            st.caption("Posted by " + post["author"])
else:
    st.info("No posts in HR yet. Share your updates!")

st.subheader("Share with HR Team")
with st.form("HRPostForm"):
    title = st.text_input("Title", key="HR_title")
    content = st.text_area("Content", key="HR_content")
    post_type = st.selectbox("Post Type", ["Policy", "Announcement", "Training", "Benefits"])
    
    if st.form_submit_button("Post to Department"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "HR", [post_type.lower()])
            st.success("Posted to HR feed!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")
