import sys
from auth import Auth
from task_manager import create_task, view_tasks, edit_task, delete_task, update_task_status

def start_app():
    # ... the rest of your code stays exactly the same
    """Member 4: Authentication Entry Point"""
    auth_system = Auth()
    
    while True:
        print("\n=== Task Management System ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            auth_system.login(username, password)
            
            
            if auth_system.current_user:
                main_menu(auth_system) 

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/user): ").lower()
            if role not in ("admin", "user"):
                print("Error: Invalid role.")
            else:
                auth_system.register(username, password, role)

        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def main_menu(auth):
    user = auth.current_user
    print(f"\nWelcome, {user['username']} ({user['role']})!")

    while True:
        print(f"\n--- Main Menu ({user['role']}) ---")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Update Task Status")
        print("6. Projects (Member 3 - Pending)")
        print("7. Logout")
        
        choice = input("Select an option: ")

        if choice == "1":
            try:
                title = input("Task title: ")
                description = input("Task description: ")
                
                task = create_task(title, description, user['username'])
                print(f"Success! Task created with ID: {task.id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            tasks = view_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                for t in tasks:
                    print(f"\nID: {t.id}")
                    print(f"Title: {t.title} | Status: {t.status}")
                    print(f"Description: {t.description}")
                    print(f"Created By: {t.created_by}")

        elif choice == "3":
            try:
                task_id = input("Task ID to edit: ")
                title = input("New title (blank to keep current): ")
                description = input("New description (blank to keep current): ")
                edit_task(task_id, 
                          title=title if title.strip() else None, 
                          description=description if description.strip() else None)
                print("Task updated successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                task_id = input("Task ID to delete: ")
                delete_task(task_id)
                print("Task deleted successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            try:
                task_id = input("Task ID: ")
                status = input("New status (Pending, In Progress, Completed): ")
                update_task_status(task_id, status)
                print("Task status updated.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("\n--- Projects ---")
            print("TODO: Waiting for Member 3 to push project assignments.")

        elif choice == "7":
            auth.logout()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    start_app()