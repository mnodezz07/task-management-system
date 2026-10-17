
# Authentication Module
The authentication module manages user registration, login, logout, and role management for the Python Task Management System.

## Responsibilities
- Register users and prevent duplicate usernames.
- Hash passwords securely using PBKDF2-HMAC and SHA-256.
- Authenticate users during login.
- Support administrator and regular user roles.
- Use the `@login_required` decorator to protect restricted functions.
- Store user information in a JSON file.

## Technologies
- Python
- JSON
- `hashlib`, `secrets`, `hmac`, and `functools`

## How to Run
```bash
python auth.py
```

## Testing
Test registration, duplicate usernames, password validation, successful and failed logins, logout, and access restrictions.

## Security
Do not upload real user credentials to GitHub. Restrict administrator creation to authorized personnel.

