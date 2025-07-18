import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import with error handling
try:
    from utils.data import load_data, save_data, add_post, is_c_suite
    
    def get_posts_for_user(user_department, user_role, user_name):
        posts = load_data("posts.json")
        visible_posts = []
        for post in posts:
            if post.get("is_vip", False):
                if (is_c_suite(user_role) or user_name in post.get("vip_recipients", []) or post["author"] == user_name):
                    visible_posts.append(post)
            elif post["department"] == "All":
                visible_posts.append(post)
            elif post["department"] == user_department:
                visible_posts.append(post)
        return visible_posts
        
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

st.title("🏠 Company-Wide Feed")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to view the feed.")
    st.stop()

user_dept = st.session_state["employee"]["department"]
user_role = st.session_state["employee"]["role"]
user_name = st.session_state["employee"]["name"]

# Display posts that user can see
visible_posts = get_posts_for_user(user_dept, user_role, user_name)

if visible_posts:
    st.subheader("Recent Updates")
    for post in reversed(visible_posts):
        # Skip VIP posts in main feed (they'll be shown separately)
        if post.get("is_vip", False):
            continue
            
        # Handle both old and new post formats
        display_author = post.get("display_author", post["author"])
        
        with st.expander(post["title"] + " - by " + display_author):
            st.write(post["content"])
            
            # Show post indicators
            if post.get("is_anonymous", False):
                st.caption("🔒 Anonymous Executive Post")
            elif post["department"] == "All":
                st.caption("📢 Company-wide post")
            else:
                st.caption("🏢 " + post["department"] + " department post")
            
            if "timestamp" in post:
                st.caption("Posted on " + post["timestamp"][:10])
            
            if not post.get("is_anonymous", False):
                st.caption("Posted by " + post["author"])
else:
    st.info("No posts yet. Be the first to share!")

# C-Suite VIP Messages Section (only for C-Suite executives)
if is_c_suite(user_role):
    st.markdown("---")
    
    # Show role-specific header
    if user_role == "Chairman":
        st.subheader("👑 Chairman's Communications")
    else:
        st.subheader("👑 C-Suite Communications")
    
    vip_posts = [post for post in reversed(visible_posts) if post.get("is_vip", False)]
    
    if vip_posts:
        # Separate anonymous and regular C-Suite messages
        anonymous_messages = [post for post in vip_posts if post.get("department") == "Anonymous-C-Suite"]
        regular_messages = [post for post in vip_posts if post.get("department") != "Anonymous-C-Suite"]
        
        # Show anonymous messages first (more urgent)
        if anonymous_messages:
            st.subheader("🚨 Anonymous Reports & Feedback")
            for post in anonymous_messages:
                # Show category if available
                category = ""
                if post.get("tags"):
                    category = post["tags"][0].replace("_", " ").title()
                    category = f" - {category}"
                
                with st.expander(f"🚨 ANONYMOUS{category}: {post['title']}"):
                    st.write(post["content"])
                    st.error("🔒 Anonymous message to C-Suite leadership")
                    if "timestamp" in post:
                        st.caption("Received on " + post["timestamp"][:10])
                    
                    # Show who this was sent to
                    if post.get("vip_recipients"):
                        st.caption("Sent to: " + ", ".join(post["vip_recipients"]))
        
        # Show regular C-Suite messages
        if regular_messages:
            st.subheader("💼 C-Suite Messages")
            for post in regular_messages:
                display_author = post.get("display_author", post["author"])
                with st.expander("👑 C-Suite: " + post["title"] + " - by " + display_author):
                    st.write(post["content"])
                    st.caption("🔒 C-Suite Executives Only")
                    if "timestamp" in post:
                        st.caption("Posted on " + post["timestamp"][:10])
                    if not post.get("is_anonymous", False):
                        st.caption("Posted by " + post["author"])
        
        if not vip_posts:
            st.info("No C-Suite messages yet.")
    else:
        st.info("No C-Suite messages yet.")

# Post Creation Form
st.markdown("---")
st.subheader("Create New Post")

# Different posting options based on role
posting_options = ["Regular Post"]

if user_role == "Executive":
    posting_options.extend(["Anonymous Executive Post", "Anonymous Message to C-Suite"])

if is_c_suite(user_role):
    posting_options.extend(["Anonymous Executive Post", "C-Suite Message", "Anonymous Message to C-Suite"])

post_type = st.selectbox("Post Type:", posting_options)

with st.form("PostForm"):
    title = st.text_input("Title")
    content = st.text_area("Content")
    
    # Regular visibility options
    if post_type == "Regular Post":
        st.write("**Who should see this post?**")
        scope = st.radio(
            "Post visibility:",
            ["My Department Only (" + user_dept + ")", "Everyone (Company-wide)"],
            help="Choose whether this post should be visible to your department only or to the entire company"
        )
        
    elif post_type == "Anonymous Executive Post":
        st.write("**Anonymous Executive Post**")
        st.info("Your name will not be displayed. Post will show as 'Anonymous Executive'")
        scope = st.radio(
            "Post visibility:",
            ["My Department Only (" + user_dept + ")", "Everyone (Company-wide)"]
        )
        
    elif post_type == "Anonymous Message to C-Suite":
        st.write("**Anonymous Message to C-Suite**")
        st.error("🔒 Anonymous message sent directly to C-Suite executives")
        st.warning("⚠️ Your identity will be completely hidden - perfect for whistleblowing or sensitive feedback")
        
        # Target specific C-Suite executives
        st.write("**Select C-Suite Recipients:**")
        chairman_recipient = st.checkbox("Chairman", help="Send to Chairman of the Board")
        ceo_recipient = st.checkbox("CEO", help="Send to Chief Executive Officer")
        president_recipient = st.checkbox("President", help="Send to Company President")
        vp_recipient = st.checkbox("Vice President", help="Send to Vice Presidents")
        group_president_recipient = st.checkbox("Group President", help="Send to Group Presidents")
        
        # Option for specific individuals
        specific_recipients = st.text_area(
            "Specific C-Suite Members (optional):",
            placeholder="Enter specific names separated by commas, e.g., John Smith, Jane Doe",
            help="Optional: Add specific C-Suite members by name"
        )
        
        # Message category for better organization
        message_category = st.selectbox(
            "Message Category:",
            ["General Feedback", "Compliance Issue", "Ethical Concern", "Financial Matter", "Strategic Suggestion", "Confidential Report", "Board Matter"]
        )
        
        scope = "Anonymous-C-Suite"
        
    elif post_type == "C-Suite Message":
        st.write("**C-Suite Message - Chairman, CEOs, Presidents, VPs Only**")
        st.error("🔒 This message will ONLY be visible to C-Suite executives (Chairman, CEOs, Presidents, VPs, Group Presidents)")
        st.warning("⚠️ Not visible to regular Admins or other employees")
        
        # Option to send to specific C-Suite executives
        specific_recipients = st.text_area(
            "Additional C-Suite Recipients (optional):",
            placeholder="Enter names separated by commas, e.g., John Smith (CEO), Jane Doe (VP)",
            help="Optional: Add specific C-Suite executives who should see this message"
        )
        
        scope = "C-Suite"
    
    if st.form_submit_button("Post"):
        if title and content:
            # Determine post settings
            is_anonymous = (post_type == "Anonymous Executive Post" or post_type == "Anonymous Message to C-Suite")
            is_vip = (post_type == "C-Suite Message" or post_type == "Anonymous Message to C-Suite")
            
            if post_type == "Anonymous Message to C-Suite":
                post_dept = "Anonymous-C-Suite"
                vip_recipients = []
                
                # Add role-based recipients
                if chairman_recipient:
                    vip_recipients.append("Chairman")
                if ceo_recipient:
                    vip_recipients.append("CEO")
                if president_recipient:
                    vip_recipients.append("President")
                if vp_recipient:
                    vip_recipients.append("Vice President")
                if group_president_recipient:
                    vip_recipients.append("Group President")
                
                # Add specific named recipients
                if specific_recipients:
                    vip_recipients.extend([name.strip() for name in specific_recipients.split(",")])
                
                # Add message category as tag
                tags = [message_category.lower().replace(" ", "_")]
                
                success_msg = "Anonymous message sent to C-Suite successfully!"
                
            elif post_type == "C-Suite Message":
                post_dept = "C-Suite"
                vip_recipients = []
                if specific_recipients:
                    vip_recipients = [name.strip() for name in specific_recipients.split(",")]
                tags = []
                success_msg = "C-Suite message posted successfully!"
                
            elif "Everyone" in scope:
                post_dept = "All"
                vip_recipients = []
                tags = []
                success_msg = "Posted to company-wide feed!"
            else:
                post_dept = user_dept
                vip_recipients = []
                tags = []
                success_msg = "Posted to " + user_dept + " department!"
            
            add_post(
                title, content, user_name, post_dept, 
                tags=tags, is_anonymous=is_anonymous, is_vip=is_vip, 
                vip_recipients=vip_recipients
            )
            st.success(success_msg)
            st.rerun()
        else:
            st.error("Please fill in both title and content")

# Show posting instructions
if is_c_suite(user_role):
    with st.expander("ℹ️ C-Suite Posting Options"):
        st.write("""
        **Regular Post**: Your name will be displayed normally to all users
        
        **Anonymous Executive Post**: Your post will show as "Anonymous Executive" - useful for sensitive feedback
        
        **C-Suite Message**: 👑 **ONLY visible to Chairman, CEOs, Presidents, VPs, and Group Presidents** - perfect for:
        - Strategic board discussions
        - Executive-only announcements
        - Confidential leadership matters
        
        **Anonymous Message to C-Suite**: 🚨 **Completely anonymous reports sent directly to C-Suite** - perfect for:
        - Whistleblowing
        - Compliance issues
        - Ethical concerns
        - Sensitive feedback to leadership
        - Board matters
        
        ⚠️ **Note**: C-Suite messages are NOT visible to regular Admins or other employees
        """)
elif user_role == "Executive":
    with st.expander("ℹ️ Executive Posting Options"):
        st.write("""
        **Regular Post**: Your name will be displayed normally
        
        **Anonymous Executive Post**: Your post will show as "Anonymous Executive" - useful for sensitive feedback
        
        **Anonymous Message to C-Suite**: 🚨 **Send anonymous reports directly to C-Suite leadership** - perfect for:
        - Whistleblowing
        - Reporting compliance issues
        - Ethical concerns
        - Sensitive feedback to leadership
        - Board matters
        
        Your identity will be completely protected. Messages can be sent to Chairman, CEO, President, VPs, etc.
        """)