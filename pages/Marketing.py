import streamlit as st
from utils.data import load_data, add_post

st.title("🧩 Marketing Department Feed")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the Marketing feed.")
    st.stop()

posts = load_data("posts.json")
dept_posts = [post for post in reversed(posts) if post["department"] == "Marketing"]

if dept_posts:
    st.subheader("Marketing Updates")
    for post in dept_posts:
        with st.expander(post["title"] + " - by " + post["author"]):
            st.write(post["content"])
            st.caption("Posted on " + post["timestamp"][:10])
else:
    st.info("No posts in Marketing yet.")

st.subheader("Share with Marketing Team")
with st.form("MarketingPostForm"):
    title = st.text_input("Title", key="Marketing_title")
    content = st.text_area("Content", key="Marketing_content")
    post_type = st.selectbox("Post Type", ["Campaign", "Analytics", "Strategy", "Update"])
    if st.form_submit_button("Post to Department"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "Marketing", [post_type.lower()])
            st.success("Posted to Marketing feed!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")
