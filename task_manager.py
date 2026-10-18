
"""Task management for the CLI project."""

import json
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path(__file__).parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"

VALID_STATUSES = ("Pending", "In Progress", "Completed")


class Task:
    """Represent a task in the task management system."""

    def __init__(
        self,
        title,
        description,
        created_by,
        assigned_to=None,
        project_id=None,
        status="Pending",
        task_id=None,
    ):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty.")

        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")

        if created_by is None or not str(created_by).strip():
            raise ValueError("Task creator is required.")

        if status not in VALID_STATUSES:
            raise ValueError(
                "Status must be Pending, In Progress, or Completed."
            )

        self.id = str(task_id or uuid4())
        self.title = title.strip()
        self.description = description.strip()
        self.created_by = str(created_by)
        self.assigned_to = (
            str(assigned_to) if assigned_to is not None else None
        )
        self.project_id = (
            str(project_id) if project_id is not None else None
        )
        self.status = status

    def to_dict(self):
        """Convert a task to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "project_id": self.project_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a task from a saved dictionary."""
        return cls(
            title=data["title"],
            description=data["description"],
            created_by=data["created_by"],
            assigned_to=data.get("assigned_to"),
            project_id=data.get("project_id"),
            status=data.get("status", "Pending"),
            task_id=data["id"],
        )


def load_tasks():
    """Load tasks from the JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("The tasks file contains invalid JSON.") from error

    if not isinstance(records, list):
        raise ValueError("The tasks file must contain a list.")

    return [Task.from_dict(record) for record in records]


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)


def create_task(
    title,
    description,
    created_by,
    assigned_to=None,
    project_id=None,
):
    """Create and save a task."""
    task = Task(
        title=title,
        description=description,
        created_by=created_by,
        assigned_to=assigned_to,
        project_id=project_id,
    )

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return task


def view_tasks():
    """Return all tasks."""
    return load_tasks()


def get_task_by_id(task_id):
    """Find a task by its ID, or return None."""
    for task in load_tasks():
        if task.id == str(task_id):
            return task
    return None


def edit_task(task_id, title=None, description=None):
    """Edit a task's title and/or description."""
    tasks = load_tasks()

    task = next(
        (item for item in tasks if item.id == str(task_id)),
        None,
    )

    if task is None:
        raise ValueError("Task not found.")

    if title is not None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty.")
        task.title = title.strip()

    if description is not None:
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")
        task.description = description.strip()

    save_tasks(tasks)
    return task


def delete_task(task_id):
    """Delete a task by its ID."""
    tasks = load_tasks()

    task = next(
        (item for item in tasks if item.id == str(task_id)),
        None,
    )

    if task is None:
        raise ValueError("Task not found.")

    tasks.remove(task)
    save_tasks(tasks)
    return task


def update_task_status(task_id, status):
    """Change a task's status."""
    if status not in VALID_STATUSES:
        raise ValueError(
            "Status must be Pending, In Progress, or Completed."
        )

    tasks = load_tasks()

    task = next(
        (item for item in tasks if item.id == str(task_id)),
        None,
    )

    if task is None:
        raise ValueError("Task not found.")

    task.status = status
    save_tasks(tasks)
    return task

def task_menu():
    while True:
        print("\n===== TASK MANAGEMENT =====")
        print("1. Create task")
        print("2. View tasks")
        print("3. Edit task")
        print("4. Delete task")
        print("5. Update task status")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input("Task title: ")
                description = input("Task description: ")
                user_id = input("Your user ID: ")

                task = create_task(title, description, user_id)
                print(f"Task created! ID: {task.id}")

            elif choice == "2":
                tasks = view_tasks()

                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        print(f"\nID: {task.id}")
                        print(f"Title: {task.title}")
                        print(f"Description: {task.description}")
                        print(f"Status: {task.status}")
                        print(f"Created by: {task.created_by}")

            elif choice == "3":
                task_id = input("Task ID to edit: ")
                title = input("New title (blank to keep current): ")
                description = input(
                    "New description (blank to keep current): "
                )

                edit_task(
                    task_id,
                    title=title if title.strip() else None,
                    description=description if description.strip() else None,
                )
                print("Task updated successfully.")

            elif choice == "4":
                task_id = input("Task ID to delete: ")
                delete_task(task_id)
                print("Task deleted successfully.")

            elif choice == "5":
                task_id = input("Task ID: ")
                print("Pending | In Progress | Completed")
                status = input("New status: ")

                update_task_status(task_id, status)
                print("Task status updated.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Please choose an option from 0 to 5.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    task_menu()
