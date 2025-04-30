import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tasks import (
    filter_tasks_by_priority,
    filter_tasks_by_category,
    generate_unique_id,
    load_tasks,
    search_tasks
)

import pytest
import json

from unittest.mock import patch, MagicMock
from datetime import datetime
import app
import tasks

@patch('app.st.rerun')
@patch('app.save_tasks')
@patch('app.load_tasks')
@patch('app.st.button')
@patch('app.st.selectbox')
@patch('app.st.checkbox')
@patch('app.st.sidebar.form')
@patch('app.st.sidebar.header')
@patch('app.st.title')
@patch('app.st.columns')

def test_complete_task(mock_columns, mock_title, mock_header, mock_form, mock_checkbox,
                       mock_selectbox, mock_button, mock_load_tasks, mock_save_tasks, mock_rerun):

    mock_load_tasks.return_value = [
        {
            "id": 1, "title": "Test Task", "description": "Desc",
            "priority": "High", "category": "Work",
            "due_date": "2025-04-30", "completed": False
        }
    ]

    mock_button.side_effect = lambda label, key=None: key == "complete_1"
    mock_columns.return_value = (MagicMock(), MagicMock())
    mock_selectbox.side_effect = lambda label, options: options[0]
    mock_checkbox.return_value = True
    mock_form.return_value.__enter__.return_value = None
    mock_form.return_value.__exit__.return_value = None
    app.main()
    mock_rerun.assert_called_once()


def test_generate_unique_id():
    tasks = [
        {"id": 1, "title": "Task 1"},
        {"id": 2, "title": "Task 2"}
    ]
    new_id = generate_unique_id(tasks)
    assert new_id == 3  

    tasks = []
    new_id = generate_unique_id(tasks)
    assert new_id == 1 

def test_load_tasks():

    tasks = load_tasks("non_existent_file.json")
    assert tasks == [], "Test failed: Expected an empty list when file does not exist."

    valid_tasks = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    with open("valid_tasks.json", "w") as f:
        json.dump(valid_tasks, f)
    tasks = load_tasks("valid_tasks.json")
    assert tasks == valid_tasks, "Test failed"
    os.remove("valid_tasks.json") 

    with open("empty_tasks.json", "w") as f:
        f.write("[]")
    tasks = load_tasks("empty_tasks.json")
    assert tasks == [], "Test failed: Expected an empty list when the file is empty."
    os.remove("empty_tasks.json")

    with open("invalid_tasks.json", "w") as f:
        f.write("{ id: 1, title: 'Task 1' }") 
    tasks = load_tasks("invalid_tasks.json")
    assert tasks == [], "Test failed"
    os.remove("invalid_tasks.json")

def test_search_tasks():
    tasks = [
        {"id": 1, "title": "Buy milk", "description": "Grocery shopping"},
        {"id": 2, "title": "Write report", "description": "Work task"}
    ]
    results = search_tasks(tasks, "milk")
    assert len(results) == 1
    assert results[0]["title"] == "Buy milk"

def test_task_creation():
    tasks = []
    task_title = "Test Task"
    task_description = "Test Description"
    task_priority = "High"
    task_category = "Work"
    task_due_date = datetime.strptime("2025-06-01", "%Y-%m-%d")

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

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test Task"
    assert tasks[0]["priority"] == "High"
    assert tasks[0]["completed"] is False







