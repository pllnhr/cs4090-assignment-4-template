import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, sort_tasks_by_created_time, filter_tasks_by_completion

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        show_completed = st.sidebar.checkbox("Show Completed Tasks", value=True)

        
        if submit_button and task_title:
            new_task = {
            "id": max([task["id"] for task in tasks], default=0) + 1,
            "title": task_title,
            "description": task_description,
            "priority": task_priority,
            "category": task_category,
            "due_date": task_due_date.strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
        
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])


    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    sort_by_time = st.selectbox("Sort by Creation Time", ["Newest First", "Oldest First"])
  
    if sort_by_time == "Newest First":
        filtered_tasks = sort_tasks_by_created_time(filtered_tasks, order="desc")
    else:
        filtered_tasks = sort_tasks_by_created_time(filtered_tasks, order="asc")
        
    filtered_tasks = filter_tasks_by_completion(filtered_tasks, show_completed=show_completed)

    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Crucial" if not task.get("crucial", False) else "Unmark", key=f"crucial_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["crucial"] = not t.get("crucial", False)
                        save_tasks(tasks)
                        st.rerun()

            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

if __name__ == "__main__":
    main()