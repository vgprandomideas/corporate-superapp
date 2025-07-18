import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

st.title("📊 Admin Command Center")
st.markdown("Monitor activity across all departments in real-time. This dashboard auto-updates based on task assignments, feedback, and post feeds.")

# Admin Check
employee = st.session_state["employee"]
if employee["role"] != "Admin":
    st.warning("⚠️ Admins only. You do not have permission to view this page.")
    st.stop()

# ---------- DATA LOADING ----------
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

tasks = load_json("data/tasks.json")
feedback = load_json("data/anonymous_feedback.json")
posts = load_json("data/posts.json")

# ---------- METRICS OVERVIEW ----------
st.subheader("📌 Quick Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", len(tasks))
col2.metric("Anonymous Feedback", len(feedback))
col3.metric("Posts Across Departments", len(posts))

st.markdown("---")

# ---------- TASK STATUS CHART ----------
st.subheader("✅ Task Completion Breakdown")
if tasks:
    task_status = pd.Series([t["status"] for t in tasks])
    fig, ax = plt.subplots()
    task_status.value_counts().plot.pie(autopct="%1.1f%%", ylabel="", ax=ax)
    st.pyplot(fig)
else:
    st.info("No tasks have been assigned yet.")

# ---------- FEEDBACK ROUTING CHART ----------
st.subheader("📥 Anonymous Feedback Routing")
if feedback:
    feedback_routes = pd.Series([f["route_to"] for f in feedback])
    fig, ax = plt.subplots()
    feedback_routes.value_counts().plot.bar(color="teal", rot=0, ax=ax)
    st.pyplot(fig)
else:
    st.info("No feedback received yet.")

# ---------- DEPARTMENT TASK DISTRIBUTION ----------
st.subheader("🏢 Tasks by Department")
if tasks:
    dept_counts = pd.Series([t["department"] for t in tasks])
    fig, ax = plt.subplots()
    dept_counts.value_counts().plot.barh(color="darkorange", ax=ax)
    st.pyplot(fig)
else:
    st.info("No department task data yet.")

# ---------- TOP USERS LEADERBOARD ----------
st.subheader("🏆 Top Task Owners")
if tasks:
    owner_counts = pd.Series([t["assigned_to"] for t in tasks])
    fig, ax = plt.subplots()
    owner_counts.value_counts().head(10).plot.bar(color="purple", rot=30, ax=ax)
    st.pyplot(fig)
else:
    st.info("No tasks assigned yet.")

# ---------- POSTS BY DEPARTMENT ----------
st.subheader("📰 Posts by Department")
if posts:
    post_depts = pd.Series([p["department"] for p in posts if "department" in p])
    fig, ax = plt.subplots()
    post_depts.value_counts().plot.bar(color="steelblue", ax=ax)
    st.pyplot(fig)
else:
    st.info("No posts found.")
