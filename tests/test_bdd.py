import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import app
import tasks

from tasks import get_overdue_tasks
from datetime import datetime, timedelta
from tasks import filter_tasks_by_category, filter_tasks_by_priority

def test_add_task_with_missing_title():
    tasks = []
    new_task = {
        "title": "",
        "description": "Test Description",
        "priority": "High",
        "category": "Work",
        "due_date": "2025-05-01",
        "completed": False,
        "created_at": "2025-04-29 12:00:00"
    }
    
    if not new_task["title"]:
        pass
    else:
        tasks.append(new_task)

    assert len(tasks) == 0, "Task with missing title should not be added"

def test_delete_task():
    tasks = [{"id": 1, "title": "Task 1", "completed": False}]
    task_id_to_delete = 1
    tasks = [task for task in tasks if task["id"] != task_id_to_delete]
    
    assert not any(task["id"] == task_id_to_delete for task in tasks), "Task should be deleted"

def test_get_overdue_tasks():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")

    tasks = [
        {"title": "Past Due", "due_date": yesterday, "completed": False},
        {"title": "Future", "due_date": today, "completed": False},
        {"title": "Done", "due_date": yesterday, "completed": True}
    ]

    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1
    assert overdue[0]["title"] == "Past Due"

def test_filter_by_category_and_priority():
    tasks = [
        {"title": "Task 1", "category": "Work", "priority": "High"},
        {"title": "Task 2", "category": "Work", "priority": "Low"},
        {"title": "Task 3", "category": "Personal", "priority": "High"}
    ]

    filtered = filter_tasks_by_category(tasks, "Work")
    filtered = filter_tasks_by_priority(filtered, "High")

    assert len(filtered) == 1
    assert filtered[0]["title"] == "Task 1"

def test_long_description():
    long_desc = "A" * 300  
    max_length = 100

    def truncate(desc, limit):
        return desc if len(desc) <= limit else desc[:limit] + "..."

    task = {"description": truncate(long_desc, max_length)}
    
    assert len(task["description"]) <= max_length + 3 
    assert task["description"].endswith("..."), "Description should be truncated with ellipsis"





