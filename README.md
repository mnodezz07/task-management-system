
# Python Task Management CLI
A Command-Line Interface (CLI) application built in Python to manage users, projects, and tasks. The system features secure user authentication, role-based access control, local JSON persistence, and a modular Object-Oriented design.

## Features
- **User Authentication:** Secure registration and login with hashed passwords.
- **Task Management:** Create, view, edit, delete, and update the status of tasks.
- **Project Management:** Create new projects and view your assigned projects.
- **Data Persistence:** All users, tasks, and projects are automatically saved to local JSON files.
- **Error Handling:** Built-in validation prevents empty tasks and invalid status updates

## Technologies
- Python 3 or Python
- JSON
- `hashlib`, `secrets`, `hmac`, and `functools` for authentication and security
- `pytest` for unit testing

## Setup Instructions
1. **Clone the repository**
     ```bash
    git clone <your-repo-url>
    cd task-management-system
    ```
2. **Install dependencies**
   ```bash
   pip install pytest
   ```
3. **To run the application**
   ```bash
   python3 main.py 
   ```
   *(or python main.py depending on your os)*
4. **Testing** 
   ```bash
   pytest
   ```


## Project Structure

```text
task-management-system/
│
├── data/                  # Local JSON storage files (tasks, users, projects)
├── models/                # OOP Class definitions (Project class)
├── tests/                 # Pytest suite (test_auth.py, test_tasks.py)
│
├── auth.py                # Authentication logic and password hashing
├── main.py                # CLI Entry point and central menu
├── project_manager.py     # Project creation and management logic
├── task_manager.py        # Task CRUD operations
├── pytest.ini             # Pytest configuration for module imports
└── README.md              # Project documentation
```