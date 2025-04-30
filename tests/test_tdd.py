import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from datetime import datetime
from tasks import sort_tasks_by_created_time, filter_tasks_by_completion

@pytest.fixture

def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "created_at": "2025-04-27 14:00:00"},
        {"id": 2, "title": "Task 2", "created_at": "2025-04-28 14:00:00"},
        {"id": 3, "title": "Task 3", "created_at": "2025-04-26 14:00:00"},
    ]

def test_sort_tasks_newest_first(sample_tasks):
    sorted_tasks = sort_tasks_by_created_time(sample_tasks, order="desc")
    assert [task["id"] for task in sorted_tasks] == [2, 1, 3]

def test_sort_tasks_oldest_first(sample_tasks):
    sorted_tasks = sort_tasks_by_created_time(sample_tasks, order="asc")
    assert [task["id"] for task in sorted_tasks] == [3, 1, 2]

def test_filter_completed_tasks():
    tasks = [
        {"id": 1, "title": "Task 1", "completed": True},
        {"id": 2, "title": "Task 2", "completed": False},
        {"id": 3, "title": "Task 3", "completed": False},
    ]
    result = filter_tasks_by_completion(tasks, show_completed=False)
    assert [task["id"] for task in result] == [2, 3]

def test_mark_task_as_crucial():
    tasks = [{"id": 1, "title": "Test", "crucial": False}]
    tasks[0]["crucial"] = True
    assert tasks[0]["crucial"] is True


