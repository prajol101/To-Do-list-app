import json
import os
from datetime import datetime
import uuid

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks, description, date=None, priority="Medium"):
    """
    Add a new task to the list.
    
    Args:
        tasks (list): The updated list of tasks.
        description (str): Task description.
        date (str): Due date (YYYY-MM-DD) or None.
        priority (str): Priority level (High, Medium, Low).
    """
    new_task = {
        "id": str(uuid.uuid4()),
        "description": description,
        "due_date": str(date) if date else None,
        "priority": priority,
        "completed": False,
        "created_at": str(datetime.now())
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return tasks

def update_task(tasks, task_id, updates):
    """
    Update a task by ID.
    
    Args:
        tasks (list): Current list of tasks.
        task_id (str): ID of the task to update.
        updates (dict): Dictionary of fields to update.
    """
    for task in tasks:
        if task["id"] == task_id:
            task.update(updates)
            break
    save_tasks(tasks)
    return tasks

def delete_task(tasks, task_id):
    """
    Delete a task by ID.
    """
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return tasks

def toggle_completion(tasks, task_id, status):
    """
    Update completion status.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = status
            break
    save_tasks(tasks)
    return tasks
