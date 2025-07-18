import streamlit as st
import json
import os
from datetime import date

# File path setup
TASKS_FILE = "data/tasks.json"
EMPLOYEES_FILE = "data/employees.json"

# Load employee data
def load_employees():
    if os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, "r") as f:
            return json.load(f)
    return []

# Load tasks
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

st.title("✅ Task Execution Board")
st.markdown("Assign detailed tasks with clear KRAs, deadlines, and outcomes.")

# Load employees and tasks
employees = load_employees()
tasks = load_tasks()

# Task creation UI
with st.expander("➕ Assign a New Task", expanded=True):
    task_title = st.text_input("Task Title")
    task_description = st.text_area("Task Description")
    expected_outcomes = st.text_area("Expected Outcomes")
    kras = st.text_area("Key Responsibility Areas (KRAs)")

    emp_map = {f"{emp['name']} ({emp['id']})": emp for emp in employees}
    assignee_display = st.selectbox("Assign to", list(emp_map.keys()))
    deadline = st.date_input("Deadline", date.today())

    if st.button("Assign Task"):
        emp = emp_map[assignee_display]
        task = {
            "title": task_title,
            "description": task_description,
            "expected_outcomes": expected_outcomes,
            "kras": kras,
            "assigned_to": emp["name"],
            "employee_id": emp["id"],
            "department": emp["department"],
            "deadline": str(deadline),
            "status": "Pending"
        }
        tasks.append(task)
        save_tasks(tasks)
        st.success("✅ Task assigned.")
