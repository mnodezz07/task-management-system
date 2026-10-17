
import json
import hashlib
import os
from functools import wraps

FILE = "users.json"


# Authentication decorator
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


# Main program
auth = Auth()

while True:
    print("\n1. Register")
    print("2. Login")
    print("3. View Profile")
    print("4. Admin Action")
    print("5. Logout")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        role = input("Role (admin/user): ").lower()

        if role not in ("admin", "user"):
            print("Invalid role.")
        else:
            auth.register(username, password, role)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        auth.login(username, password)

    elif choice == "3":
        auth.view_profile()

    elif choice == "4":
        auth.admin_action()

    elif choice == "5":
        auth.logout()

    elif choice == "0":
        break

    else:
        print("Invalid choice.")
