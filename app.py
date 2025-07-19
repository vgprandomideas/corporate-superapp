# app.py - Your working app with visual enhancements
import streamlit as st
from utils.auth import login_user
import os

# ---- Set page config with enhanced settings ----
st.set_page_config(
    page_title="Corporate Superapp", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏢"
)

# ---- Modern CSS Styling ----
def load_visual_enhancements():
    """Add modern visual styling to your existing app"""
    st.markdown("""
    <style>
    /* Import beautiful fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global enhancements */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Enhanced sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 0 15px 15px 0;
    }
    
    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Beautiful user profile card */
    .user-profile-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .user-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-role {
        font-size: 0.9rem;
        color: #667eea;
        font-weight: 500;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        padding: 0.4rem 1rem;
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(5px);
    }
    
    /* Enhanced navigation */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stRadio > div > label {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin: 0.3rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        cursor: pointer;
        font-weight: 500;
    }
    
    .stRadio > div > label:hover {
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(255,255,255,0.9));
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01);
    }
    
    /* Enhanced main content */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
    }
    
    /* Beautiful page headers */
    h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h2, h3 {
        color: #2c3e50;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced cards and containers */
    .stContainer, .stColumn {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Beautiful expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        margin: 0.5rem 0;
    }
    
    .streamlit-expanderHeader:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(255,255,255,0.95));
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.8) 100%);
        border-radius: 0 0 12px 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-top: none;
        backdrop-filter: blur(10px);
    }
    
    /* Enhanced form elements */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 1);
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        padding: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: rgba(255, 255, 255, 1);
    }
    
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        backdrop-filter: blur(5px);
    }
    
    /* Enhanced notifications */
    .stSuccess {
        background: linear-gradient(135deg, #2ed573, #1e90ff);
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(46, 213, 115, 0.3);
    }
    
    .stError {
        background: linear-gradient(135deg, #ff4757, #c44569);
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ffa502, #ff6348);
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(255, 165, 2, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3742fa, #2f3542);
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(55, 66, 250, 0.3);
    }
    
    /* Enhanced metrics */
    .metric-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 0.5rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Logo enhancement */
    .logo-container img {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .logo-container img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Animation classes */
    .fade-in-up {
        animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .user-profile-card {
            padding: 1rem;
        }
        
        .stButton > button {
            padding: 0.7rem 1rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    </style>
    """, unsafe_allow_html=True)

# Load the visual enhancements
load_visual_enhancements()

# ---- Login handling (keep your existing logic) ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_user()
    st.stop()

# ---- After login (keep your existing logic) ----
employee = st.session_state["employee"]
employee_name = employee["name"]
department = employee["department"]
role = employee["role"]

# ---- Enhanced Sidebar ----
with st.sidebar:
    # Enhanced Company Branding
    st.markdown("""
    <div class="logo-container" style="text-align: center; margin-bottom: 1.5rem;">
        <img src="https://placehold.co/180x80/667eea/ffffff?text=Corporate+Logo" width="180">
    </div>
    """, unsafe_allow_html=True)

    # Enhanced User Info
    st.markdown(f"""
    <div class="user-profile-card fade-in-up">
        <div class="user-name">👋 {employee_name}</div>
        <div class="user-role">{department} – {role}</div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Navigation
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        label="Go to:",
        options=[
            "🏠 Home Feed",
            "📢 Campaigns",
            f"🧩 {department} Space",
            "📊 Dashboard",
            "✅ Tasks",
            "🔒 Anonymous Feedback",
            "🤝 Collaboration",
            "📞 Video Room",
            "📅 Schedule Meeting"
        ],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Quick Actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Post"):
            st.success("📝 Post form ready!")
    
    with col2:
        if st.button("✅ Task"):
            st.success("✅ Task form ready!")

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---- Keep your existing page mapping logic ----
page_map = {
    "🏠 Home Feed": "pages/Home.py",
    "📢 Campaigns": "pages/Campaigns.py",
    "📊 Dashboard": "pages/Dashboard.py",
    "✅ Tasks": "pages/Tasks.py",
    "🔒 Anonymous Feedback": "pages/Anonymous.py",
    f"🧩 {department} Space": f"pages/{department}.py",
    "🤝 Collaboration": "pages/Collaboration.py",
    "📞 Video Room": "pages/VideoRoom.py",
    "📅 Schedule Meeting": "pages/ScheduleMeeting.py"
}

# ---- Enhanced Page Loader (keep your working logic but make it safer) ----
st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)

try:
    if os.path.exists(page_map[page]):
        with open(page_map[page], "r", encoding="utf-8") as f:
            exec(f.read())
    else:
        st.error(f"❌ Page file not found: {page_map[page]}")
        st.info("Please check if all page files exist in the pages/ directory.")
except Exception as e:
    st.error(f"❌ Error loading **{page}**: {e}")
    st.info("🔄 Please refresh the page or contact support.")

st.markdown('</div>', unsafe_allow_html=True)

# ---- Enhanced Footer ----
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem;">
    <div class="fade-in-up">
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">
            © 2025 Corporate Superapp | Enhanced with Modern UI ✨
        </p>
        <p style="color: #8e9aaf; font-size: 0.8rem; margin: 0.5rem 0 0 0;">
            🚀 Secure • 🎨 Beautiful • ⚡ Fast
        </p>
    </div>
</div>
""", unsafe_allow_html=True)