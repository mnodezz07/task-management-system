import json
import os

class ProjectManager:
    def __init__(self, filepath="data/projects.json"):
        self.filepath = filepath

    def _load_data(self):
        if not os.path.exists(self.filepath):
            if os.path.dirname(self.filepath):
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w") as file:
                json.dump([], file)
            return []
        with open(self.filepath, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def create_project(self, title, description, due_date, user_username):
        from models.project import Project
        projects = self._load_data()
        
        new_project = Project(title, description, due_date, user_username)
        projects.append(new_project.to_dict())
        
        self._save_data(projects)
        return new_project

    def get_user_projects(self, user_username):
        projects = self._load_data()
        return [p for p in projects if p["user_username"] == user_username]

    def assign_task_to_project(self, project_id, task_id):
        projects = self._load_data()
        for p in projects:
            if p["project_id"] == project_id:
                if task_id not in p["task_ids"]:
                    p["task_ids"].append(task_id)
                    self._save_data(projects)
                    return True
        return False
