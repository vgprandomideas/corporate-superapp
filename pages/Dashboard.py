# pages/Dashboard.py - Fixed version without matplotlib
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

st.title("📊 Admin Command Center")
st.markdown("Monitor activity across all departments in real-time. This dashboard auto-updates based on task assignments, feedback, and post feeds.")

# Admin Check
employee = st.session_state["employee"]
if employee["role"] not in ["Admin", "Executive", "Chairman", "CEO", "President", "Vice President"]:
    st.warning("⚠️ Admin access required. You do not have permission to view this page.")
    st.info(f"Your current role: {employee['role']}")
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

tasks = load_json("tasks.json")
feedback = load_json("feedback.json")
posts = load_json("posts.json")
meetings = load_json("scheduled_meetings.json")

# ---------- METRICS OVERVIEW ----------
st.subheader("📌 Quick Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Tasks", len(tasks), delta=None)
with col2:
    st.metric("Anonymous Feedback", len(feedback), delta=None)
with col3:
    st.metric("Posts Across Departments", len(posts), delta=None)
with col4:
    st.metric("Scheduled Meetings", len(meetings), delta=None)

st.markdown("---")

# ---------- ENHANCED CHARTS WITH PLOTLY ----------

# Task Status Chart
st.subheader("✅ Task Completion Breakdown")
if tasks:
    task_status_data = {}
    for task in tasks:
        status = task.get("status", "Unknown")
        task_status_data[status] = task_status_data.get(status, 0) + 1
    
    if task_status_data:
        fig_pie = px.pie(
            values=list(task_status_data.values()),
            names=list(task_status_data.keys()),
            title="Task Status Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            font_size=14,
            title_font_size=18,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No tasks have been assigned yet.")

# Department Task Distribution
st.subheader("🏢 Tasks by Department")
if tasks:
    dept_data = {}
    for task in tasks:
        dept = task.get("department", "Unknown")
        dept_data[dept] = dept_data.get(dept, 0) + 1
    
    if dept_data:
        fig_bar = px.bar(
            x=list(dept_data.keys()),
            y=list(dept_data.values()),
            title="Task Distribution by Department",
            color=list(dept_data.values()),
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(
            xaxis_title="Department",
            yaxis_title="Number of Tasks",
            font_size=14,
            title_font_size=18
        )
        st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No department task data yet.")

# Feedback Routing Chart
st.subheader("📥 Anonymous Feedback Routing")
if feedback:
    feedback_data = {}
    for fb in feedback:
        route = fb.get("route_to", "Unknown")
        feedback_data[route] = feedback_data.get(route, 0) + 1
    
    if feedback_data:
        fig_feedback = px.bar(
            x=list(feedback_data.keys()),
            y=list(feedback_data.values()),
            title="Feedback Distribution by Department",
            color=list(feedback_data.values()),
            color_continuous_scale="Teal"
        )
        fig_feedback.update_layout(
            xaxis_title="Department",
            yaxis_title="Number of Feedback",
            font_size=14,
            title_font_size=18
        )
        st.plotly_chart(fig_feedback, use_container_width=True)
else:
    st.info("No feedback received yet.")

# Posts by Department
st.subheader("📰 Posts by Department")
if posts:
    post_data = {}
    for post in posts:
        dept = post.get("department", "Unknown")
        post_data[dept] = post_data.get(dept, 0) + 1
    
    if post_data:
        fig_posts = px.bar(
            x=list(post_data.keys()),
            y=list(post_data.values()),
            title="Posts Distribution by Department",
            color=list(post_data.values()),
            color_continuous_scale="Viridis"
        )
        fig_posts.update_layout(
            xaxis_title="Department",
            yaxis_title="Number of Posts",
            font_size=14,
            title_font_size=18
        )
        st.plotly_chart(fig_posts, use_container_width=True)
else:
    st.info("No posts found.")

# ---------- RECENT ACTIVITY ----------
st.subheader("📈 Recent Activity")

# Combine recent posts and tasks
recent_activity = []

# Recent posts
for post in sorted(posts, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]:
    recent_activity.append({
        "Type": "📝 Post",
        "Title": post["title"],
        "Author/Assignee": post.get("display_author", post["author"]),
        "Department": post["department"],
        "Timestamp": post.get("timestamp", "")[:16].replace("T", " ")
    })

# Recent tasks
for task in sorted(tasks, key=lambda x: x.get("created_at", x.get("timestamp", "")), reverse=True)[:5]:
    recent_activity.append({
        "Type": "✅ Task",
        "Title": task["title"],
        "Author/Assignee": task["assigned_to"],
        "Department": task["department"],
        "Timestamp": task.get("created_at", task.get("timestamp", ""))[:16].replace("T", " ")
    })

# Sort by timestamp and display
if recent_activity:
    recent_df = pd.DataFrame(recent_activity)
    recent_df = recent_df.sort_values("Timestamp", ascending=False).head(10)
    st.dataframe(recent_df, use_container_width=True, hide_index=True)
else:
    st.info("No recent activity to display.")

# ---------- SYSTEM STATS ----------
st.subheader("🔧 System Statistics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Data Summary**")
    st.write(f"• Total Users: {len(load_json('employees.json'))}")
    st.write(f"• Active Posts: {len([p for p in posts if p.get('department') != 'Archived'])}")
    st.write(f"• Pending Tasks: {len([t for t in tasks if t.get('status') == 'Pending'])}")
    st.write(f"• Unread Feedback: {len([f for f in feedback if f.get('status') == 'unread'])}")

with col2:
    st.markdown("**🏢 Department Activity**")
    if posts:
        most_active_dept = max(post_data, key=post_data.get) if post_data else "N/A"
        st.write(f"• Most Active Dept: {most_active_dept}")
    if tasks:
        busiest_assignee = max(set([t["assigned_to"] for t in tasks]), 
                              key=lambda x: len([t for t in tasks if t["assigned_to"] == x]))
        st.write(f"• Busiest Employee: {busiest_assignee}")
    st.write(f"• Total Meetings: {len(meetings)}")

# ---------- ADMIN ACTIONS ----------
st.markdown("---")
st.subheader("⚙️ Admin Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

with col2:
    if st.button("📊 Export Analytics", use_container_width=True):
        # Create analytics export
        analytics_data = {
            "tasks": len(tasks),
            "posts": len(posts),
            "feedback": len(feedback),
            "meetings": len(meetings)
        }
        st.download_button(
            label="Download Analytics JSON",
            data=json.dumps(analytics_data, indent=2),
            file_name="analytics_export.json",
            mime="application/json"
        )

with col3:
    if st.button("🧹 Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache cleared!")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("📊 Dashboard updates automatically. Data refreshed on page reload.")