import streamlit as st
from utils.data import load_data, add_post

st.set_page_config(page_title="Engineering Department", layout="wide")
st.title("🧩 Engineering Department Feed")

# Authentication check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("🔒 Please log in to access the Engineering department.")
    st.stop()

# Load department-specific posts
posts = load_data("posts.json")
dept_posts = [post for post in reversed(posts) if post["department"] == "Engineering"]

# Display existing posts
if dept_posts:
    st.subheader("📢 Engineering Updates")
    for post in dept_posts:
        with st.expander(f"{post['title']} – by {post['author']}"):
            st.write(post["content"])
            st.caption(f"📅 {post['timestamp'][:10]}")
else:
    st.info("🚧 No posts yet in Engineering.")

# Submission form for new post
st.subheader("✍️ Share an Update with the Engineering Team")
with st.form("EngineeringPostForm"):
    title = st.text_input("Post Title", key="Engineering_title")
    content = st.text_area("Write your post here...", key="Engineering_content")
    post_type = st.selectbox("Select Post Type", ["Update", "Question", "Announcement", "Resource"])

    if st.form_submit_button("📤 Post to Engineering"):
        if title and content:
            add_post(
                title=title,
                content=content,
                author=st.session_state["employee"]["name"],
                department="Engineering",
                tags=[post_type.lower()]
            )
            st.success("✅ Successfully posted to the Engineering feed!")
            st.rerun()
        else:
            st.error("⚠️ Please fill out both title and content before submitting.")
