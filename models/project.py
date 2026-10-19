import uuid

class Project:
    def __init__(self, title, description, due_date, user_username):
        self.project_id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_username = user_username
        self.task_ids = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Project title must be a non-empty string.")
        self._title = value

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_username": self.user_username,
            "task_ids": self.task_ids
        }
