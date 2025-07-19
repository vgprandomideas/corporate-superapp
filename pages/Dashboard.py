# pages/Dashboard.py - Perfect version with fixed layout and Plotly
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Plotly import - suppress warnings
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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

.chart-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
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
        except Exception:
            data[key] = []
    
    return data

# Load all data
dashboard_data = load_dashboard_data()

tasks = dashboard_data["tasks"]
feedback = dashboard_data["feedback"]
posts = dashboard_data["posts"]
meetings = dashboard_data["meetings"]
employees = dashboard_data["employees"]

# ---------- KEY PERFORMANCE INDICATORS ----------
st.subheader("📈 Key Performance Indicators")

# Calculate metrics
total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t.get("status") == "Completed"])
pending_tasks = len([t for t in tasks if t.get("status") == "Pending"])
completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
total_posts = len(posts)
unread_feedback = len([f for f in feedback if f.get("status") == "unread"])
active_employees = len(set([t.get("assigned_to") for t in tasks if t.get("assigned_to")]))

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

# ---------- ANALYTICS DASHBOARD WITH TABS ----------
st.subheader("📊 Analytics Dashboard")

# Create tabs for different analytics views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Task Analytics", "🏢 Department Insights", "📬 Feedback Analysis", "📱 Activity Monitor"])

with tab1:
    st.markdown("### 📈 Task Performance Analytics")
    
    if tasks:
        col1, col2 = st.columns(2)
        
        with col1:
            # Task Status Analysis
            status_counts = {}
            for task in tasks:
                status = task.get("status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if PLOTLY_AVAILABLE and status_counts:
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
            else:
                # HTML fallback
                st.markdown("""
                <div class="chart-container">
                    <h4>📊 Task Status Distribution</h4>
                """, unsafe_allow_html=True)
                
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
        
        with col2:
            # Department Distribution
            dept_counts = {}
            for task in tasks:
                dept = task.get("department", "Unknown")
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
            if PLOTLY_AVAILABLE and dept_counts:
                fig_bar = px.bar(
                    x=list(dept_counts.keys()),
                    y=list(dept_counts.values()),
                    title="🏢 Tasks by Department",
                    color=list(dept_counts.values()),
                    color_continuous_scale="Blues"
                )
                fig_bar.update_layout(height=400, xaxis_title="Department", yaxis_title="Number of Tasks")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                # HTML fallback
                st.markdown("**🏢 Tasks by Department**")
                for dept, count in dept_counts.items():
                    percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
                    st.write(f"• **{dept}**: {count} ({percentage:.1f}%)")
    else:
        st.info("📝 No tasks available for analysis")

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
            # Department performance chart
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
    else:
        st.info("📊 No department data available")

with tab3:
    st.markdown("### 📬 Feedback Analysis Center")
    
    if feedback:
        col1, col2 = st.columns(2)
        
        with col1:
            feedback_routes = {}
            for fb in feedback:
                route = fb.get("route_to", "Unknown")
                feedback_routes[route] = feedback_routes.get(route, 0) + 1
            
            if PLOTLY_AVAILABLE and feedback_routes:
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
                st.markdown("**📥 Feedback Distribution**")
                for route, count in feedback_routes.items():
                    percentage = (count / len(feedback) * 100) if len(feedback) > 0 else 0
                    st.write(f"• **{route}**: {count} ({percentage:.1f}%)")
        
        with col2:
            # Feedback status analysis
            status_counts = {}
            for fb in feedback:
                status = fb.get("status", "unread")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if PLOTLY_AVAILABLE and status_counts:
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
                    st.write(f"• **{status}**: {count} ({percentage:.1f}%)")
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
        activity_df = pd.DataFrame(all_activity[:20])  # Show top 20
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
    else:
        st.info("📱 No recent activity to display")

# ---------- ADMIN ACTIONS (MOVED TO BOTTOM) ----------
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
        with st.expander("🛠️ System Information"):
            st.json({
                "current_admin": user_name,
                "admin_role": user_role,
                "charts_engine": "Plotly" if PLOTLY_AVAILABLE else "HTML",
                "data_files": {
                    "tasks": len(tasks),
                    "posts": len(posts),
                    "feedback": len(feedback),
                    "employees": len(employees)
                },
                "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

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
        Admin: {user_name} | Role: {user_role} | Charts: {"Interactive Plotly" if PLOTLY_AVAILABLE else "HTML Fallback"} | Status: Online ✅
    </p>
</div>
""", unsafe_allow_html=True)