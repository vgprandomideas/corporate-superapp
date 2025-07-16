import streamlit as st
from utils.data import load_data, save_data, add_post

st.title("🧩 Finance Department Feed")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the Finance feed.")
    st.stop()

posts = load_data("posts.json")
dept_posts = [post for post in reversed(posts) if post["department"] == "Finance"]

if dept_posts:
    st.subheader("Finance Updates")
    for post in dept_posts:
        with st.expander(post["title"] + " - by " + post["author"]):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
            st.caption("Posted by " + post["author"])
else:
    st.info("No posts in Finance yet. Share your updates!")

st.subheader("Share with Finance Team")
with st.form("FinancePostForm"):
    title = st.text_input("Title", key="Finance_title")
    content = st.text_area("Content", key="Finance_content")
    post_type = st.selectbox("Post Type", ["Budget", "Report", "Update", "Analysis"])
    
    if st.form_submit_button("Post to Department"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "Finance", 
                    [post_type.lower()])
            st.success("Posted to Finance feed!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")