import streamlit as st
from utils.data import load_data, save_data, add_post

st.title("🧩 Engineering Department Feed")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the Engineering feed.")
    st.stop()

# Display department posts
posts = load_data("posts.json")
dept_posts = [post for post in reversed(posts) if post["department"] == "Engineering"]

if dept_posts:
    st.subheader("Engineering Updates")
    for post in dept_posts:
        with st.expander(post["title"] + " - by " + post["author"]):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
            st.caption("Posted by " + post["author"])
else:
    st.info("No posts in Engineering yet. Share your updates!")

# Post form
st.subheader("Share with Engineering Team")
with st.form("EngineeringPostForm"):
    title = st.text_input("Title", key="Engineering_title")
    content = st.text_area("Content", key="Engineering_content")
    post_type = st.selectbox("Post Type", ["Update", "Question", "Announcement", "Resource"])
    
    if st.form_submit_button("Post to Department"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "Engineering", 
                    [post_type.lower()])
            st.success("Posted to Engineering feed!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")