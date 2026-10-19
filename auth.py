
import json
import hashlib
import os
from functools import wraps

FILE = "data/users.json"



def login_required(func):
    @wraps(func)
    def wrapper(auth, *args, **kwargs):
        if auth.current_user is None:
            print("Please log in first.")
            return

        return func(auth, *args, **kwargs)
    return wrapper


class Auth:
    def __init__(self):
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        if os.path.exists(FILE):
            with open(FILE, "r") as file:
                return json.load(file)
        return []

    def save_users(self):
        with open(FILE, "w") as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, role="user"):
        for user in self.users:
            if user["username"] == username:
                print("Username already exists.")
                return

        new_user = {
            "username": username,
            "password": self.hash_password(password),
            "role": role
        }

        self.users.append(new_user)
        self.save_users()
        print("Registration successful!")

    def login(self, username, password):
        for user in self.users:
            if (
                user["username"] == username
                and user["password"] == self.hash_password(password)
            ):
                self.current_user = user
                print("Login successful!")
                print("Role:", user["role"])
                return

        print("Invalid username or password.")

    def logout(self):
        self.current_user = None
        print("Logged out.")

    @login_required
    def view_profile(self):
        print("Username:", self.current_user["username"])
        print("Role:", self.current_user["role"])

    @login_required
    def admin_action(self):
        if self.current_user["role"] != "admin":
            print("Access denied. Admin only.")
            return

        print("Welcome, Admin!")


