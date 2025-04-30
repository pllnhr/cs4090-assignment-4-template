import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from datetime import datetime
from tasks import filter_tasks_by_completion, filter_tasks_by_category, filter_tasks_by_priority

def test_filter_completed_tasks():
    tasks = [
        {"id": 1, "title": "Task 1", "completed": True},
        {"id": 2, "title": "Task 2", "completed": False},
        {"id": 3, "title": "Task 3", "completed": False},
    ]
    result = filter_tasks_by_completion(tasks, show_completed=False)
    assert [task["id"] for task in result] == [2, 3]

def test_filter_tasks_by_category():
    tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "Home"},
        {"id": 3, "category": "Personal"},
        {"id": 4, "category": "Work"},
        {"id": 5, "category": "Home"}
    ]

    work_tasks = filter_tasks_by_category(tasks, "Work")
    assert len(work_tasks) == 2
    for task in work_tasks:
        assert task["category"] == "Work"

    home_tasks = filter_tasks_by_category(tasks, "Home")
    assert len(home_tasks) == 2
    for task in home_tasks:
        assert task["category"] == "Home"

    personal_tasks = filter_tasks_by_category(tasks, "Personal")
    assert len(personal_tasks) == 1
    assert personal_tasks[0]["category"] == "Personal"

def test_filter_tasks_by_priority():
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "Low"}
    ]
    high_priority_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0]["priority"] == "High"

    medium_priority_tasks = filter_tasks_by_priority(tasks, "Medium")
    assert len(medium_priority_tasks) == 1
    assert medium_priority_tasks[0]["priority"] == "Medium"

    low_priority_tasks = filter_tasks_by_priority(tasks, "Low")
    assert len(low_priority_tasks) == 1
    assert low_priority_tasks[0]["priority"] == "Low"

    invalid_priority_tasks = filter_tasks_by_priority(tasks, "Invalid")
    assert invalid_priority_tasks == []

