import pytest
from auth import Auth

def test_user_registration(tmp_path, monkeypatch):
  
    test_file = tmp_path / "users.json"
    monkeypatch.setattr("auth.FILE", str(test_file))

    auth = Auth()
    auth.register("testuser", "password123", "user")
    
    assert len(auth.users) == 1
    assert auth.users[0]["username"] == "testuser"
    assert auth.users[0]["password"] != "password123" 

def test_login_success(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    monkeypatch.setattr("auth.FILE", str(test_file))

    auth = Auth()
    auth.register("admin", "securepass", "admin")
    auth.login("admin", "securepass")
    
    assert auth.current_user is not None
    assert auth.current_user["role"] == "admin"