# pages/Dashboard.py - Fixed with safe imports
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Safe plotly import with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available. Using basic charts.")

# Session state check
try:
    employee = st.session_state["employee"]
    user_role = employee.get("role", "Unknown")
    user_name = employee.get("name", "Unknown")
    user_dept = employee.get("department", "Unknown")
except KeyError:
    st.error("🔒 Authentication Required")
    st.warning("Please login first to access the Admin Dashboard.")
    st.info("👈 Click 'Home Feed' in the sidebar to return to login.")
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
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.progress-bar {
    width: 100%;
    height: 20px;
    background-color: #e9ecef;
    border-radius: 10px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
}

.chart-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.status-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.2rem;
}

.status-completed { background: #2ed573; color: white; }
.status-pending { background: #ffa502; color: white; }
.status-overdue { background: #ff4757; color: white; }
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
    st.stop()

# ---------- DATA LOADING ----------
@st.cache_data(ttl=300)
def load_dashboard_data():
    """Load all dashboard data with caching"""
    data = {}
    
    files = {
        "tasks": "tasks.json",
        "feedback": "feedback.json", 
        "posts": "posts.json",
        "meetings": "scheduled_meetings.json",
        "employees": "employees.json"
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
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #667eea; margin: 0;">📋 Total Tasks</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{total_tasks}</h2>
        <p style="color: #6c757d; margin: 0;">Active: {pending_tasks}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    delta_color = "#2ed573" if completion_rate >= 75 else "#ffa502" if completion_rate >= 50 else "#ff4757"
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #2ed573; margin: 0;">✅ Completion Rate</h3>
        <h2 style="color: {delta_color}; margin: 0.5rem 0;">{completion_rate:.1f}%</h2>
        <p style="color: #6c757d; margin: 0;">Target: 75%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #ff4757; margin: 0;">🔔 Feedback</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{len(feedback)}</h2>
        <p style="color: #6c757d; margin: 0;">Unread: {unread_feedback}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3742fa; margin: 0;">📝 Posts</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{total_posts}</h2>
        <p style="color: #6c757d; margin: 0;">All Departments</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #ffa502; margin: 0;">👥 Active Users</h3>
        <h2 style="color: #2c3e50; margin: 0.5rem 0;">{active_employees}</h2>
        <p style="color: #6c757d; margin: 0;">Engaged</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- ANALYTICS SECTION ----------
st.subheader("📊 Analytics Dashboard")

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Task Analytics", "🏢 Department Insights", "📬 Feedback Analysis", "📱 Activity Monitor"])

with tab1:
    st.markdown("### 📈 Task Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Task Status Analysis
        if tasks and PLOTLY_AVAILABLE:
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
            fig_pie.update_layout(height=400, font_size=14, title_font_size=18)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        elif tasks:
            # Fallback: HTML progress bars
            st.markdown("""
            <div class="chart-container">
                <h4>📊 Task Status Distribution</h4>
            """, unsafe_allow_html=True)
            
            status_counts = {}
            for task in tasks:
                status = task.get("status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in status_counts.items():
                percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
                
                if status == "Completed":
                    bar_color = "#2ed573"
                elif status == "Pending":
                    bar_color = "#ffa502"
                else:
                    bar_color = "#ff4757"
                
                st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>{status}</strong></span>
                        <span>{count} ({percentage:.1f}%)</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {percentage}%; background: {bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("📝 No tasks available for analysis")
    
    with col2:
        # Task Priority Distribution
        if tasks and PLOTLY_AVAILABLE:
            priority_counts = {}
            for task in tasks:
                priority = task.get("priority", "Medium")
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            if priority_counts:
                colors = {"High": "#ff4757", "Medium": "#ffa502", "Low": "#2ed573"}
                fig_priority = px.bar(
                    x=list(priority_counts.keys()),
                    y=list(priority_counts.values()),
                    title="🎯 Task Priority Distribution",
                    color=list(priority_counts.keys()),
                    color_discrete_map=colors
                )
                fig_priority.update_layout(height=400, xaxis_title="Priority Level", yaxis_title="Number of Tasks", showlegend=False)
                st.plotly_chart(fig_priority, use_container_width=True)
        
        elif tasks:
            # Fallback for priority
            st.markdown("""
            <div class="chart-container">
                <h4>🎯 Task Priority Distribution</h4>
            """, unsafe_allow_html=True)
            
            priority_counts = {"High": 0, "Medium": 0, "Low": 0}
            for task in tasks:
                priority = task.get("priority", "Medium")
                if priority in priority_counts:
                    priority_counts[priority] += 1
            
            colors = {"High": "#ff4757", "Medium": "#ffa502", "Low": "#2ed573"}
            
            for priority, count in priority_counts.items():
                percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
                
                st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><strong>{priority}</strong></span>
                        <span>{count} ({percentage:.1f}%)</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {percentage}%; background: {colors[priority]};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🏢 Department Performance Insights")
    
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
        
        if PLOTLY_AVAILABLE:
            # Create department performance chart
            dept_names = list(dept_stats.keys())
            completed_tasks_by_dept = [dept_stats[dept]["completed"] for dept in dept_names]
            pending_tasks_by_dept = [dept_stats[dept]["pending"] for dept in dept_names]
            
            fig_dept = go.Figure()
            fig_dept.add_trace(go.Bar(name='Completed', x=dept_names, y=completed_tasks_by_dept, marker_color='#2ed573'))
            fig_dept.add_trace(go.Bar(name='Pending', x=dept_names, y=pending_tasks_by_dept, marker_color='#ffa502'))
            
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
        col1, col2 = st.columns(2)
        
        with col1:
            feedback_routes = {}
            for fb in feedback:
                route = fb.get("route_to", "Unknown")
                feedback_routes[route] = feedback_routes.get(route, 0) + 1
            
            if PLOTLY_AVAILABLE:
                fig_feedback = px.bar(
                    x=list(feedback_routes.keys()),
                    y=list(feedback_routes.values()),
                    title="📥 Feedback Distribution by Route",
                    color=list(feedback_routes.values()),
                    color_continuous_scale="Reds"
                )
                fig_feedback.update_layout(height=400)
                st.plotly_chart(fig_feedback, use_container_width=True)
            else:
                # Fallback feedback chart
                st.markdown("**📥 Feedback Distribution**")
                for route, count in feedback_routes.items():
                    percentage = (count / len(feedback) * 100) if len(feedback) > 0 else 0
                    st.markdown(f"• **{route}**: {count} ({percentage:.1f}%)")
        
        with col2:
            # Feedback status analysis
            status_counts = {}
            for fb in feedback:
                status = fb.get("status", "unread")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if PLOTLY_AVAILABLE:
                fig_status = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="📊 Feedback Status Overview",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_status.update_layout(height=400)
                st.plotly_chart(fig_status, use_container_width=True)
            else:
                st.markdown("**📊 Feedback Status**")
                for status, count in status_counts.items():
                    percentage = (count / len(feedback) * 100) if len(feedback) > 0 else 0
                    st.markdown(f"• **{status}**: {count} ({percentage:.1f}%)")
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
            "Title": post.get("title", "Unknown")[:40] + "..." if len(post.get("title", "")) > 40 else post.get("title", "Unknown"),
            "User": post.get("author", "Unknown"),
            "Department": post.get("department", "Unknown"),
            "Timestamp": post.get("timestamp", "Unknown")[:16].replace("T", " ") if post.get("timestamp") else "Unknown"
        })
    
    # Add recent tasks
    for task in sorted(tasks, key=lambda x: x.get("created_at", x.get("timestamp", "")), reverse=True)[:10]:
        all_activity.append({
            "Type": "✅ Task",
            "Title": task.get("title", "Unknown")[:40] + "..." if len(task.get("title", "")) > 40 else task.get("title", "Unknown"),
            "User": task.get("assigned_to", "Unknown"),
            "Department": task.get("department", "Unknown"),
            "Timestamp": task.get("created_at", task.get("timestamp", "Unknown"))[:16].replace("T", " ") if task.get("created_at") or task.get("timestamp") else "Unknown"
        })
    
    # Sort all activity by timestamp
    all_activity.sort(key=lambda x: x["Timestamp"], reverse=True)
    
    if all_activity:
        st.markdown("### 🔄 Live Activity Feed")
        activity_df = pd.DataFrame(all_activity[:20])  # Show top 20
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
    else:
        st.info("📱 No recent activity to display")

# ---------- ADMIN ACTIONS ----------
st.markdown("---")
st.subheader("🛠️ Admin Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
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
            "generated_by": user_name,
            "generated_at": datetime.now().isoformat()
        }
        
        st.download_button(
            label="📥 Download Analytics Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"admin_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

with col3:
    if st.button("🧹 Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Cache cleared successfully!")

with col4:
    if st.button("🔧 System Info", use_container_width=True):
        with st.expander("🛠️ Debug Information"):
            debug_info = {
                "current_admin": user_name,
                "admin_role": user_role,
                "plotly_available": PLOTLY_AVAILABLE,
                "data_files_status": {
                    "tasks.json": f"{len(tasks)} records",
                    "posts.json": f"{len(posts)} records", 
                    "feedback.json": f"{len(feedback)} records",
                    "employees.json": f"{len(employees)} records"
                },
                "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.json(debug_info)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; 
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.2);">
    <p style="margin: 0; color: #6c757d;">
        🚀 <strong>Corporate Superapp Admin Dashboard</strong> - Enhanced Analytics Platform
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #8e9aaf;">
        Admin: {user_name} | Role: {user_role} | Charts: {"Plotly" if PLOTLY_AVAILABLE else "HTML"} | Status: Online ✅
    </p>
</div>
""", unsafe_allow_html=True)