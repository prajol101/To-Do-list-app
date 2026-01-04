import streamlit as st
import pandas as pd
from datetime import date
from utils import load_tasks, add_task, update_task, delete_task, toggle_completion

# Page Configuration
st.set_page_config(
    page_title="Streamlit To-Do App",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .stCheckbox {
        margin-top: 10px;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<p class="main-header">✅ Modern To-Do List</p>', unsafe_allow_html=True)

    # Initialize Session State
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    # --- Sidebar ---
    st.sidebar.header("🎯 Options")
    
    # Filter functionality
    filter_status = st.sidebar.radio(
        "Filter Tasks:",
        ["All", "Incomplete", "Completed"]
    )
    
    # Sort functionality (simple implementation)
    sort_by = st.sidebar.selectbox(
        "Sort By:",
        ["Created Date", "Priority", "Due Date"]
    )

    # Stats
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t['completed']])
    incomplete_tasks = total_tasks - completed_tasks
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Statistics")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Pending", incomplete_tasks)
    col2.metric("Done", completed_tasks)
    st.sidebar.progress(completed_tasks / total_tasks if total_tasks > 0 else 0)

    # --- Main Content ---
    
    # Add New Task Section
    with st.expander("➕ Add New Task", expanded=False):
        with st.form("add_task_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_task_desc = st.text_input("Task Description", placeholder="What needs to be done?")
            with col2:
                new_task_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
            
            new_task_date = st.date_input("Due Date", min_value=date.today())
            
            submitted = st.form_submit_button("Add Task")
            if submitted:
                if new_task_desc.strip():
                    st.session_state.tasks = add_task(
                        st.session_state.tasks, 
                        new_task_desc, 
                        new_task_date, 
                        new_task_priority
                    )
                    st.success("Task added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a task description.")

    st.markdown("---")

    # Display Tasks
    tasks_to_show = st.session_state.tasks

    # Apply Filters
    if filter_status == "Incomplete":
        tasks_to_show = [t for t in tasks_to_show if not t['completed']]
    elif filter_status == "Completed":
        tasks_to_show = [t for t in tasks_to_show if t['completed']]

    # Apply Sort
    if sort_by == "Priority":
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        tasks_to_show.sort(key=lambda x: priority_map.get(x['priority'], 1))
    elif sort_by == "Due Date":
        tasks_to_show.sort(key=lambda x: x['due_date'] if x['due_date'] else '9999-12-31')
    else: # Created Date
        tasks_to_show.sort(key=lambda x: x['created_at'], reverse=True)


    if not tasks_to_show:
        st.info("No tasks found matching your criteria! 🎉")
    else:
        for i, task in enumerate(tasks_to_show):
            # Using a container for each task for better layout control
            with st.container():
                # Define columns for list layout
                c1, c2, c3, c4 = st.columns([0.5, 4, 1.5, 1])
                
                # Checkbox for completion
                is_completed = c1.checkbox(
                    "Complete", 
                    value=task['completed'], 
                    key=f"check_{task['id']}",
                    label_visibility="collapsed"
                )
                
                # Update state if checkbox changed
                if is_completed != task['completed']:
                    st.session_state.tasks = toggle_completion(st.session_state.tasks, task['id'], is_completed)
                    st.rerun()

                # Task Description (Strikethrough if completed)
                task_text = task['description']
                if task['completed']:
                    task_text = f"<s>{task_text}</s>"
                
                c2.markdown(f"**{task_text}**", unsafe_allow_html=True)
                
                # Priority Badge
                priority_color = {
                    "High": "red",
                    "Medium": "orange",
                    "Low": "green"
                }
                c2.caption(f"📅 Due: {task['due_date']} | Priority: :{priority_color[task['priority']]}[{task['priority']}]")

                # Action Buttons (Edit/Delete) in Expander or Columns
                # Using an expander for "Edit" to keep list clean
                with c3.expander("Edit"):
                    with st.form(key=f"edit_{task['id']}"):
                        edit_desc = st.text_input("Desc", value=task['description'])
                        edit_date = st.date_input("Date", value=pd.to_datetime(task['due_date']).date() if task['due_date'] else date.today())
                        edit_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task['priority']))
                        
                        if st.form_submit_button("Save"):
                            st.session_state.tasks = update_task(
                                st.session_state.tasks, 
                                task['id'], 
                                {
                                    "description": edit_desc, 
                                    "due_date": str(edit_date), 
                                    "priority": edit_priority
                                }
                            )
                            st.rerun()
                
                # Delete Button
                if c4.button("🗑️", key=f"del_{task['id']}", help="Delete Task"):
                    st.session_state.tasks = delete_task(st.session_state.tasks, task['id'])
                    st.rerun()
                
                st.markdown("---")

if __name__ == "__main__":
    main()
