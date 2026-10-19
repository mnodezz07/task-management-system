import pytest
from project_manager import ProjectManager

def test_create_project(tmp_path):
    
    test_file = tmp_path / "projects.json"
    
    
    pm = ProjectManager(filepath=str(test_file))
    
   
    project = pm.create_project("Test Project", "Description", "2026-12-31", "testuser")
    assert project.title == "Test Project"
    assert project.user_username == "testuser"
    
    
    user_projects = pm.get_user_projects("testuser")
    assert len(user_projects) == 1
    assert user_projects[0]["title"] == "Test Project"