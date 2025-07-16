import streamlit as st
from utils.data import load_data, save_data, add_post

st.title("🏠 Company-Wide Feed")

# Display posts
posts = load_data("posts.json")
company_posts = [post for post in reversed(posts) if post["department"] == "All"]

if company_posts:
    st.subheader("Recent Company Updates")
    for post in company_posts:
        with st.expander(post["title"] + " - by " + post["author"]):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
            st.caption("Posted by " + post["author"])
else:
    st.info("No company-wide posts yet. Be the first to share!")

# Post form
st.subheader("Share with Everyone")
with st.form("PostForm"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    if st.form_submit_button("Post"):
        if title and content:
            add_post(title, content, st.session_state["employee"]["name"], "All")
            st.success("Posted successfully!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")