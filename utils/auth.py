# utils/auth.py - Enhanced authentication with modern UI
import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = "corporate_superapp_salt_2025"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def load_users():
    """Load users from employees.json with password support"""
    if os.path.exists("employees.json"):
        with open("employees.json", "r") as f:
            employees = json.load(f)
    else:
        employees = []
    
    # Add default passwords for existing users
    default_users = [
        {"id": "EMP001", "name": "Guruprasad", "department": "Engineering", "role": "Executive", "password": "admin123"},
        {"id": "EMP002", "name": "Meera", "department": "Marketing", "role": "Manager", "password": "user123"},
        {"id": "EMP003", "name": "Ravi", "department": "HR", "role": "Recruiter", "password": "hr123"}
    ]
    
    # Merge with existing employees
    for default_user in default_users:
        existing = next((emp for emp in employees if emp["id"] == default_user["id"]), None)
        if existing:
            existing["password"] = default_user["password"]
        else:
            employees.append(default_user)
    
    return employees

def authenticate_user(username: str, password: str):
    """Authenticate user with username/password"""
    users = load_users()
    
    for user in users:
        if (user["name"].lower() == username.lower() or 
            user["id"].lower() == username.lower()):
            # For demo purposes, using simple password check
            # In production, use hashed passwords
            if user.get("password") == password:
                return user
    
    return None

def login_user():
    """Enhanced login interface"""
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        color: #667eea;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .login-subtitle {
        color: #2c3e50;
        font-size: 1.8rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    
    .login-description {
        color: #6c757d;
        margin: 0;
    }
    
    .demo-credentials {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    
    .credential-item {
        display: flex;
        justify-content: space-between;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .credential-label {
        font-weight: 600;
        color: #495057;
    }
    
    .credential-value {
        color: #667eea;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-title">🏢</div>
                <h2 class="login-subtitle">Corporate Superapp</h2>
                <p class="login-description">Welcome to your modernized workspace</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 🔐 Login to Continue")
            
            username = st.text_input(
                "👤 Username or Employee ID", 
                placeholder="Enter your name or ID",
                help="Use your name (e.g., 'Guruprasad') or Employee ID (e.g., 'EMP001')"
            )
            
            password = st.text_input(
                "🔒 Password", 
                type="password",
                placeholder="Enter your password",
                help="Default passwords are provided below for demo"
            )
            
            col_login, col_guest = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button(
                    "🚀 Login", 
                    use_container_width=True,
                    type="primary"
                )
            
            with col_guest:
                guest_button = st.form_submit_button(
                    "👀 Guest Mode", 
                    use_container_width=True,
                    help="Login as Guruprasad (Executive)"
                )
            
            # Handle login
            if login_button:
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.employee = {
                            "id": user["id"],
                            "name": user["name"],
                            "department": user["department"],
                            "role": user["role"]
                        }
                        st.success(f"✅ Welcome back, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please check username and password.")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            # Handle guest login
            if guest_button:
                guest_user = {
                    "id": "EMP001",
                    "name": "Guruprasad",
                    "department": "Engineering", 
                    "role": "Executive"
                }
                st.session_state.logged_in = True
                st.session_state.employee = guest_user
                st.success("✅ Logged in as Guest (Guruprasad)")
                st.rerun()
        
        # Demo credentials
        st.markdown("""
        <div class="demo-credentials">
            <h4 style="margin: 0 0 1rem 0; color: #495057;">🎯 Demo Credentials</h4>
            <div class="credential-item">
                <span class="credential-label">Executive:</span>
                <span class="credential-value">Guruprasad / admin123</span>
            </div>
            <div class="credential-item">
                <span class="credential-label">Manager:</span>
                <span class="credential-value">Meera / user123</span>
            </div>
            <div class="credential-item">
                <span class="credential-label">HR:</span>
                <span class="credential-value">Ravi / hr123</span>
            </div>
            <div class="credential-item">
                <span class="credential-label">Employee ID:</span>
                <span class="credential-value">EMP001, EMP002, EMP003</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick setup for new departments
        with st.expander("➕ Quick Login for Other Departments"):
            st.markdown("**Create a quick account for testing:**")
            
            quick_col1, quick_col2 = st.columns(2)
            
            with quick_col1:
                quick_name = st.text_input("Your Name")
                quick_dept = st.selectbox("Department", [
                    "Engineering", "Design", "HR", "Finance", 
                    "Marketing", "Ops", "Sales", "Legal"
                ])
            
            with quick_col2:
                quick_role = st.selectbox("Role", [
                    "Employee", "Manager", "Executive", "Admin",
                    "Chairman", "CEO", "President", "Vice President"
                ])
            
            if st.button("🎯 Quick Login", use_container_width=True):
                if quick_name and quick_dept and quick_role:
                    quick_user = {
                        "id": f"QCK_{hash(quick_name) % 1000:03d}",
                        "name": quick_name,
                        "department": quick_dept,
                        "role": quick_role
                    }
                    st.session_state.logged_in = True
                    st.session_state.employee = quick_user
                    st.success(f"✅ Quick login successful! Welcome, {quick_name}")
                    st.rerun()
                else:
                    st.warning("⚠️ Please fill in all fields")

# Session management functions
def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get("logged_in", False)

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get("employee", {})

def logout_user():
    """Logout current user"""
    for key in ["logged_in", "employee"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.error("🔒 Please log in to access this page")
            login_user()
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(allowed_roles):
    """Decorator to require specific roles"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_logged_in():
                st.error("🔒 Please log in to access this page")
                login_user()
                st.stop()
            
            user = get_current_user()
            if user.get("role") not in allowed_roles:
                st.error(f"⚠️ Access denied. Required roles: {', '.join(allowed_roles)}")
                st.info(f"Your role: {user.get('role', 'Unknown')}")
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator