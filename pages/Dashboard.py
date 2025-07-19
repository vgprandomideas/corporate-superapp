# pages/Dashboard.py - Complete Enhanced Dashboard (300+ lines)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import numpy as np

# Session state check with better error handling
try:
    employee = st.session_state["employee"]
    user_role = employee.get("role", "Unknown")
    user_name = employee.get("name", "Unknown")
    user_dept = employee.get("department", "Unknown")
except KeyError:
    st.error("🔒 Authentication Required")
    st.warning("Please login first to access the Admin Dashboard.")
    st.info("👈 Click 'Home Feed' in the sidebar to return to login.")
    st.markdown("---")
    st.markdown("### 🚀 Dashboard Features (Login Required)")
    st.markdown("""
    - **📊 Real-time Analytics** - Task, feedback, and post metrics
    - **📈 Interactive Charts** - Plotly visualizations with drill-down
    - **🏢 Department Insights** - Cross-departmental performance analysis
    - **📱 Advanced Reporting** - Export capabilities and data insights
    - **⚡ Live Monitoring** - Real-time activity feeds and notifications
    - **🎯 Performance KPIs** - Task completion rates and productivity metrics
    """)
    st.stop()

# Enhanced page styling
st.markdown("""
<style>
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: 0.5rem;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.chart-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.activity-feed {
    max-height: 400px;
    overflow-y: auto;
    border-radius: 10px;
    border: 1px solid rgba(102, 126, 234, 0.2);
}

.admin-action-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 1.5rem;
    transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown(f"""
<div class="dashboard-header">
    <h1>📊 Admin Command Center</h1>
    <p>Real-time monitoring and analytics for corporate operations</p>
    <p><strong>Welcome, {user_name}</strong> | Role: {user_role} | Department: {user_dept}</p>
</div>
""", unsafe_allow_html=True)

# Admin Role Verification
admin_roles = ["Admin", "Executive", "Chairman", "CEO", "President", "Vice President", "Group President"]

if user_role not in admin_roles:
    st.error("🚫 Access Denied - Administrative Privileges Required")
    st.warning(f"Your current role: **{user_role}** does not have admin access.")
    st.info("Required roles: " + " • ".join(admin_roles))
    
    # Show what they're missing
    st.markdown("### 🎯 Admin Dashboard Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📊 Analytics & Reporting:**
        - Real-time task completion metrics
        - Department performance analysis
        - User engagement tracking
        - Productivity insights
        """)
    with col2:
        st.markdown("""
        **🛠️ Management Tools:**
        - System monitoring dashboard
        - Data export capabilities
        - Advanced filtering options
        - Administrative controls
        """)
    st.stop()

# ---------- ENHANCED DATA LOADING ----------
@st.cache_data(ttl=300)
def load_dashboard_data():
    """Load all dashboard data with caching"""
    data = {}
    
    files = {
        "tasks": "tasks.json",
        "feedback": "feedback.json", 
        "posts": "posts.json",
        "meetings": "scheduled_meetings.json",
        "employees": "employees.json",
        "chat": "chat.json"
    }
    
    for key, filename in files.items():
        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    data[key] = json.load(f)
            else:
                data[key] = []
        except Exception as e:
            st.error(f"Error loading {filename}: {e}")
            data[key] = []
    
    return data

# Load all data
with st.spinner("🔄 Loading dashboard data..."):
    dashboard_data = load_dashboard_data()

tasks = dashboard_data["tasks"]
feedback = dashboard_data["feedback"]
posts = dashboard_data["posts"]
meetings = dashboard_data["meetings"]
employees = dashboard_data["employees"]
chat_data = dashboard_data["chat"]

# ---------- KEY PERFORMANCE INDICATORS ----------
st.subheader("📈 Key Performance Indicators")

# Calculate advanced metrics
total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t.get("status") == "Completed"])
pending_tasks = len([t for t in tasks if t.get("status") == "Pending"])
overdue_tasks = len([t for t in tasks if t.get("status") == "Overdue"])
completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

active_employees = len(set([t.get("assigned_to") for t in tasks if t.get("assigned_to")]))
total_posts = len(posts)
unread_feedback = len([f for f in feedback if f.get("status") == "unread"])

# Enhanced metrics display
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #667eea; margin: 0;">📋 Total Tasks</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{}</h2>
        <p style="color: #6c757d; margin: 0;">Active: {}</p>
    </div>
    """.format(total_tasks, pending_tasks), unsafe_allow_html=True)

with col2:
    delta_color = "green" if completion_rate >= 75 else "orange" if completion_rate >= 50 else "red"
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #2ed573; margin: 0;">✅ Completion Rate</h3>
        <h2 style="color: {}; margin: 0.5rem 0;">{:.1f}%</h2>
        <p style="color: #6c757d; margin: 0;">Target: 75%</p>
    </div>
    """.format(delta_color, completion_rate), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #ff4757; margin: 0;">🔔 Feedback</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{}</h2>
        <p style="color: #6c757d; margin: 0;">Unread: {}</p>
    </div>
    """.format(len(feedback), unread_feedback), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #3742fa; margin: 0;">📝 Posts</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{}</h2>
        <p style="color: #6c757d; margin: 0;">All Departments</p>
    </div>
    """.format(total_posts), unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #ffa502; margin: 0;">👥 Active Users</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{}</h2>
        <p style="color: #6c757d; margin: 0;">Engaged</p>
    </div>
    """.format(active_employees), unsafe_allow_html=True)

st.markdown("---")

# ---------- ADVANCED ANALYTICS SECTION ----------
st.subheader("📊 Advanced Analytics Dashboard")

# Create tabs for different analytics views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Task Analytics", "🏢 Department Insights", "📬 Feedback Analysis", "📱 Activity Monitor", "⚙️ System Health"])

with tab1:
    st.markdown("### 📈 Task Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Task Status Pie Chart
        if tasks:
            status_counts = {}
            for task in tasks:
                status = task.get("status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_pie = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="📊 Task Status Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                height=400,
                font_size=14,
                title_font_size=18,
                showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📝 No tasks available for analysis")
    
    with col2:
        # Task Priority Distribution
        if tasks:
            priority_counts = {}
            for task in tasks:
                priority = task.get("priority", "Medium")
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            colors = {"High": "#ff4757", "Medium": "#ffa502", "Low": "#2ed573"}
            fig_priority = px.bar(
                x=list(priority_counts.keys()),
                y=list(priority_counts.values()),
                title="🎯 Task Priority Distribution",
                color=list(priority_counts.keys()),
                color_discrete_map=colors
            )
            fig_priority.update_layout(
                height=400,
                xaxis_title="Priority Level",
                yaxis_title="Number of Tasks",
                showlegend=False
            )
            st.plotly_chart(fig_priority, use_container_width=True)
    
    # Task Timeline Analysis
    if tasks:
        st.markdown("### 📅 Task Timeline Analysis")
        
        # Process task dates
        task_dates = []
        for task in tasks:
            deadline = task.get("deadline")
            created = task.get("created_at", task.get("timestamp"))
            
            if deadline:
                task_dates.append({
                    "Task": task["title"][:30] + "..." if len(task["title"]) > 30 else task["title"],
                    "Created": created[:10] if created else "Unknown",
                    "Deadline": deadline,
                    "Status": task.get("status", "Unknown"),
                    "Priority": task.get("priority", "Medium"),
                    "Assignee": task.get("assigned_to", "Unassigned")
                })
        
        if task_dates:
            timeline_df = pd.DataFrame(task_dates)
            st.dataframe(timeline_df, use_container_width=True, hide_index=True)
        else:
            st.info("No task timeline data available")

with tab2:
    st.markdown("### 🏢 Department Performance Insights")
    
    # Department Task Distribution
    if tasks:
        dept_stats = {}
        for task in tasks:
            dept = task.get("department", "Unknown")
            if dept not in dept_stats:
                dept_stats[dept] = {"total": 0, "completed": 0, "pending": 0}
            
            dept_stats[dept]["total"] += 1
            if task.get("status") == "Completed":
                dept_stats[dept]["completed"] += 1
            elif task.get("status") == "Pending":
                dept_stats[dept]["pending"] += 1
        
        # Create department performance chart
        dept_names = list(dept_stats.keys())
        total_tasks = [dept_stats[dept]["total"] for dept in dept_names]
        completed_tasks = [dept_stats[dept]["completed"] for dept in dept_names]
        pending_tasks = [dept_stats[dept]["pending"] for dept in dept_names]
        
        fig_dept = go.Figure()
        fig_dept.add_trace(go.Bar(name='Completed', x=dept_names, y=completed_tasks, marker_color='#2ed573'))
        fig_dept.add_trace(go.Bar(name='Pending', x=dept_names, y=pending_tasks, marker_color='#ffa502'))
        
        fig_dept.update_layout(
            title='📊 Department Task Performance',
            xaxis_title='Department',
            yaxis_title='Number of Tasks',
            barmode='stack',
            height=400
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        
        # Department efficiency table
        st.markdown("### 📈 Department Efficiency Metrics")
        efficiency_data = []
        for dept, stats in dept_stats.items():
            efficiency = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            efficiency_data.append({
                "Department": dept,
                "Total Tasks": stats["total"],
                "Completed": stats["completed"],
                "Pending": stats["pending"],
                "Efficiency %": f"{efficiency:.1f}%"
            })
        
        efficiency_df = pd.DataFrame(efficiency_data)
        st.dataframe(efficiency_df, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### 📬 Feedback Analysis Center")
    
    if feedback:
        # Feedback routing analysis
        col1, col2 = st.columns(2)
        
        with col1:
            feedback_routes = {}
            for fb in feedback:
                route = fb.get("route_to", "Unknown")
                feedback_routes[route] = feedback_routes.get(route, 0) + 1
            
            fig_feedback = px.bar(
                x=list(feedback_routes.keys()),
                y=list(feedback_routes.values()),
                title="📥 Feedback Distribution by Route",
                color=list(feedback_routes.values()),
                color_continuous_scale="Reds"
            )
            fig_feedback.update_layout(height=400)
            st.plotly_chart(fig_feedback, use_container_width=True)
        
        with col2:
            # Feedback status analysis
            status_counts = {}
            for fb in feedback:
                status = fb.get("status", "unread")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="📊 Feedback Status Overview",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_status.update_layout(height=400)
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Recent feedback display
        st.markdown("### 📝 Recent Feedback Summary")
        recent_feedback = sorted(feedback, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
        
        feedback_display = []
        for fb in recent_feedback:
            feedback_display.append({
                "Route": fb.get("route_to", "Unknown"),
                "Content": fb.get("text", "")[:100] + "..." if len(fb.get("text", "")) > 100 else fb.get("text", ""),
                "Status": fb.get("status", "unread"),
                "Date": fb.get("timestamp", "Unknown")[:10] if fb.get("timestamp") else "Unknown"
            })
        
        if feedback_display:
            feedback_df = pd.DataFrame(feedback_display)
            st.dataframe(feedback_df, use_container_width=True, hide_index=True)
    else:
        st.info("📬 No feedback data available yet")

with tab4:
    st.markdown("### 📱 Real-time Activity Monitor")
    
    # Combine all activity
    all_activity = []
    
    # Add recent posts
    for post in sorted(posts, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]:
        all_activity.append({
            "Type": "📝 Post",
            "Title": post.get("title", "Unknown"),
            "User": post.get("author", "Unknown"),
            "Department": post.get("department", "Unknown"),
            "Timestamp": post.get("timestamp", "Unknown")[:16].replace("T", " ") if post.get("timestamp") else "Unknown"
        })
    
    # Add recent tasks
    for task in sorted(tasks, key=lambda x: x.get("created_at", x.get("timestamp", "")), reverse=True)[:10]:
        all_activity.append({
            "Type": "✅ Task",
            "Title": task.get("title", "Unknown"),
            "User": task.get("assigned_to", "Unknown"),
            "Department": task.get("department", "Unknown"),
            "Timestamp": task.get("created_at", task.get("timestamp", "Unknown"))[:16].replace("T", " ") if task.get("created_at") or task.get("timestamp") else "Unknown"
        })
    
    # Add recent feedback
    for fb in sorted(feedback, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]:
        all_activity.append({
            "Type": "💬 Feedback",
            "Title": f"Feedback to {fb.get('route_to', 'Unknown')}",
            "User": "Anonymous",
            "Department": fb.get("route_to", "Unknown"),
            "Timestamp": fb.get("timestamp", "Unknown")[:16].replace("T", " ") if fb.get("timestamp") else "Unknown"
        })
    
    # Sort all activity by timestamp
    all_activity.sort(key=lambda x: x["Timestamp"], reverse=True)
    
    if all_activity:
        st.markdown("### 🔄 Live Activity Feed")
        activity_df = pd.DataFrame(all_activity[:20])  # Show top 20
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
        
        # Activity timeline chart
        activity_by_hour = {}
        for activity in all_activity:
            try:
                hour = activity["Timestamp"][:13]  # YYYY-MM-DD HH
                activity_by_hour[hour] = activity_by_hour.get(hour, 0) + 1
            except:
                continue
        
        if len(activity_by_hour) > 1:
            fig_timeline = px.line(
                x=list(activity_by_hour.keys()),
                y=list(activity_by_hour.values()),
                title="📈 Activity Timeline (Hourly)",
                markers=True
            )
            fig_timeline.update_layout(
                xaxis_title="Time",
                yaxis_title="Activities",
                height=300
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("📱 No recent activity to display")

with tab5:
    st.markdown("### ⚙️ System Health & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Data Statistics**")
        st.write(f"• Total Employees: {len(employees)}")
        st.write(f"• Total Posts: {len(posts)}")
        st.write(f"• Total Tasks: {len(tasks)}")
        st.write(f"• Total Feedback: {len(feedback)}")
        st.write(f"• Total Meetings: {len(meetings)}")
        st.write(f"• Chat Messages: {len(chat_data)}")
        
        # System health score
        health_score = 100
        if unread_feedback > 10:
            health_score -= 20
        if pending_tasks > total_tasks * 0.7:
            health_score -= 15
        if completion_rate < 50:
            health_score -= 25
        
        health_color = "green" if health_score >= 80 else "orange" if health_score >= 60 else "red"
        st.markdown(f"**🏥 System Health Score:** <span style='color: {health_color}; font-weight: bold;'>{health_score}%</span>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**👥 User Engagement**")
        if employees:
            dept_distribution = {}
            role_distribution = {}
            for emp in employees:
                dept = emp.get("department", "Unknown")
                role = emp.get("role", "Unknown")
                dept_distribution[dept] = dept_distribution.get(dept, 0) + 1
                role_distribution[role] = role_distribution.get(role, 0) + 1
            
            st.write("**Departments:**")
            for dept, count in dept_distribution.items():
                st.write(f"• {dept}: {count}")
            
            st.write("**Roles:**")
            for role, count in role_distribution.items():
                st.write(f"• {role}: {count}")

# ---------- ADVANCED ADMIN ACTIONS ----------
st.markdown("---")
st.subheader("🛠️ Advanced Admin Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 Refresh All Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col2:
    if st.button("📊 Export Analytics", use_container_width=True):
        export_data = {
            "summary": {
                "total_tasks": total_tasks,
                "completion_rate": completion_rate,
                "total_posts": total_posts,
                "total_feedback": len(feedback),
                "active_employees": active_employees
            },
            "department_stats": dept_stats if 'dept_stats' in locals() else {},
            "generated_by": user_name,
            "generated_at": datetime.now().isoformat(),
            "system_health": health_score if 'health_score' in locals() else 100
        }
        
        st.download_button(
            label="📥 Download Full Analytics Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"admin_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col3:
    if st.button("🧹 Clear System Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ All caches cleared successfully!")

with col4:
    if st.button("🔧 Debug Information", use_container_width=True):
        with st.expander("🛠️ System Debug Information"):
            debug_info = {
                "session_state_keys": list(st.session_state.keys()),
                "current_admin": user_name,
                "admin_role": user_role,
                "data_files_status": {
                    "tasks.json": f"{len(tasks)} records",
                    "posts.json": f"{len(posts)} records", 
                    "feedback.json": f"{len(feedback)} records",
                    "employees.json": f"{len(employees)} records"
                },
                "working_directory": os.getcwd(),
                "python_version": f"{st.__version__}",
                "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.json(debug_info)

# ---------- FOOTER WITH SYSTEM INFO ----------
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"📊 Dashboard Version: 2.0.0")
    st.caption(f"🔄 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.caption(f"👤 Admin: {user_name}")
    st.caption(f"🏢 Department: {user_dept}")

with col3:
    st.caption(f"⚡ System Status: Online")
    st.caption(f"🔒 Security: Authenticated")

st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; 
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.2);">
    <p style="margin: 0; color: #6c757d;">
        🚀 <strong>Corporate Superapp Admin Dashboard</strong> - Real-time monitoring and analytics
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #8e9aaf;">
        Built with ❤️ using Streamlit • Enhanced UI/UX • Enterprise Grade
    </p>
</div>
""", unsafe_allow_html=True)