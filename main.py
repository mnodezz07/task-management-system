import sys
from auth import Auth, login_required
from task_manager import create_task, view_tasks, edit_task, delete_task, update_task_status
from project_manager import ProjectManager

def start_app():
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
            # role = input("Role (admin/user): ").lower()
            # if role not in ("admin", "user"):
            #     print("Error: Invalid role.")
            # else:
            auth_system.register(username, password, role= "user")

        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
@login_required
def main_menu(auth):
    user = auth.current_user
    pm = ProjectManager() 
    
    print(f"\nWelcome, {user['username']} ({user['role']})!")

    while True:
        print(f"\n--- Main Menu ({user['role']}) ---")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Update Task Status")
        print("6. Manage Projects") 
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
                    print(f"\nID: {t.id} | Title: {t.title} | Status: {t.status}")
                    print(f"Description: {t.description}")
                    print(f"Created By: {t.created_by}")

        elif choice == "3":
            try:
                task_id = input("Task ID to edit: ")
                title = input("New title (blank to keep current): ")
                description = input("New description (blank to keep current): ")
                edit_task(task_id, title=title if title.strip() else None, description=description if description.strip() else None)
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
            print("1. Create Project")
            print("2. View My Projects")
            proj_choice = input("Select: ")
            
            if proj_choice == "1":
                try:
                    title = input("Project Title: ")
                    desc = input("Description: ")
                    due = input("Due Date: ")
                    new_proj = pm.create_project(title, desc, due, user['username'])
                    print(f"Success! Project created with ID: {new_proj.project_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif proj_choice == "2":
                user_projects = pm.get_user_projects(user['username'])
                if not user_projects:
                    print("You have no projects.")
                else:
                    for p in user_projects:
                        print(f"\nID: {p['project_id']} | Title: {p['title']}")
                        print(f"Due: {p['due_date']} | Tasks Assigned: {len(p['task_ids'])}")

        elif choice == "7":
            auth.logout()
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    start_app()
