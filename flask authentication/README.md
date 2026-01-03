# 🔐 Flask Authentication System

A secure Flask-based authentication system implementing **password hashing, salting, encryption concepts, and session-based authentication** using industry best practices.

---

## 🚀 Features

- User Registration & Login
- Secure Password Hashing (PBKDF2 + SHA256)
- Automatic Password Salting
- Session Management with Flask-Login
- Protected Routes (`@login_required`)
- SQLite Database with SQLAlchemy ORM
- Flash Messages for UX feedback

---

## 🛡️ Security Concepts Covered

### 🔹 Password Hashing
Passwords are never stored in plain text. They are hashed using:

