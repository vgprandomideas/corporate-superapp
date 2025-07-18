import streamlit as st

def login_user():
    st.title("Corporate Superapp Login")
    st.write("Welcome to the Corporate Communication Platform")
    
    with st.form("login_form"):
        name = st.text_input("Enter your name:")
        department = st.selectbox("Select your department:", 
                                ["Engineering", "Design", "HR", "Finance", "Marketing", "Ops"])
        role = st.selectbox("Select your role:", [
            "Executive", 
            "Admin",
            "Chairman",
            "CEO",
            "President", 
            "Vice President",
            "Group President"
        ])
        
        if st.form_submit_button("Login"):
            if name.strip():
                st.session_state.logged_in = True
                st.session_state.employee = {
                    "name": name.strip(),
                    "department": department,
                    "role": role
                }
                st.success("Welcome, " + name + "!")
                st.rerun()
            else:
                st.error("Please enter your name")
