import streamlit as st
from utils.data import load_data
from collections import Counter

st.title("📊 Dashboard")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the dashboard.")
    st.stop()

posts = load_data("posts.json")
total = len(posts)
dept = st.session_state["employee"]["department"]
employee_name = st.session_state["employee"]["name"]

# Filter posts
my_posts = [p for p in posts if p["author"] == employee_name]
dept_posts = [p for p in posts if p["department"] == dept]
campaigns = [p for p in posts if "campaign" in p.get("tags", [])]

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Posts", total)
with col2:
    st.metric(dept + " Dept Posts", len(dept_posts))
with col3:
    st.metric("My Contributions", len(my_posts))
with col4:
    st.metric("Active Campaigns", len(campaigns))

# Department breakdown
st.subheader("Posts by Department")
dept_counts = Counter([p["department"] for p in posts])
for dept_name, count in dept_counts.items():
    st.write("**" + dept_name + "**: " + str(count) + " posts")

# Recent activity
st.subheader("My Recent Posts")
if my_posts:
    for post in list(reversed(my_posts))[:5]:  # Show last 5 posts
        with st.expander(post["title"] + " (" + post["department"] + ")"):
            st.write(post["content"])
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
else:
    st.info("You haven't posted anything yet.")

# Top contributors
st.subheader("Top Contributors")
author_counts = Counter([p["author"] for p in posts])
top_authors = author_counts.most_common(5)
for author, count in top_authors:
    st.write("**" + author + "**: " + str(count) + " posts")