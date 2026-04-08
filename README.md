# TaskFlow — Task Management System

A full-stack Task Management System built with **Django + Django Templates + MySQL**.

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3.10+, Django 4.2            |
| Frontend   | Django Templates, HTML/CSS/JS       |
| Database   | MySQL 8.x                           |
| Auth       | Django Session Auth      |
| ORM        | Django ORM                          |

---

## Features

- **User Registration & Login** — secure session-based auth, hashed passwords
- **Personal Tasks** — created by a user, only visible to them, fully editable
- **Assigned Tasks** — assign tasks to other users with role-based permissions
- **Role-Based Permissions:**
  - **Creator (Personal):** full CRUD on own tasks
  - **Assigner:** can set/update due date; cannot change status
  - **Assignee:** can only update task status; cannot touch other fields
- **Task Fields:** Title, Description, Status, Priority, Due Date
- **Filters:** by status, priority, type (personal / assigned by me / assigned to me)
- **Dashboard** with live stats

---

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- MySQL 8.x running locally
- `pip` and `virtualenv`

### 2. Clone / extract the project

```bash
cd taskflow
```

### 3. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `mysqlclient` requires MySQL dev libraries.
> - Ubuntu/Debian: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
> - macOS (Homebrew): `brew install mysql-client pkg-config`
> - Windows: Install MySQL Connector and set env vars as per [mysqlclient docs](https://github.com/PyMySQL/mysqlclient)

### 5. Create the MySQL database

```sql
CREATE DATABASE taskmanager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Configure the database

Edit `taskmanager/settings.py` and update the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taskmanager_db',
        'USER': 'root',           # your MySQL username
        'PASSWORD': 'yourpass',   # your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 7. Run migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations tasks
python manage.py migrate
```

### 8. Create a superuser (optional, for Django admin)

```bash
python manage.py createsuperuser
```

### 9. Create sample users (seed)

```bash
python manage.py shell
```

```python
from accounts.models import User

u1 = User.objects.create_user(username='alice', email='alice@example.com', password='Alice@1234')
u2 = User.objects.create_user(username='bob', email='bob@example.com', password='Bob@1234')
print("Users created:", u1, u2)
exit()
```

### 10. Start the development server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## Sample User Credentials

| Username | Password    | Email               |
|----------|-------------|---------------------|
| alice    | Alice@1234  | alice@example.com   |
| bob      | Bob@1234    | bob@example.com     |

---

## Database Schema

```
users (accounts_user)
  id, username, email, password, bio, date_joined, ...

tasks (tasks_task)
  id
  title          VARCHAR(255)
  description    TEXT
  status         ENUM(todo, in_progress, done)
  priority       ENUM(low, medium, high)
  due_date       DATE
  created_by_id  FK → users.id
  assigned_to_id FK → users.id (nullable)
  created_at     DATETIME
  updated_at     DATETIME
```

---

## API Endpoints (URL Map)

| URL                        | View              | Description              |
|----------------------------|-------------------|--------------------------|
| `/`                        | login_view        | Redirects to login       |
| `/login/`                  | login_view        | User login               |
| `/register/`               | register_view     | User registration        |
| `/logout/`                 | logout_view       | Logout                   |
| `/profile/`                | profile_view      | User profile             |
| `/dashboard/`              | dashboard         | Main dashboard           |
| `/tasks/create/`           | task_create       | Create new task          |
| `/tasks/<id>/`             | task_detail       | View task detail         |
| `/tasks/<id>/edit/`        | task_edit         | Edit task (role-based)   |
| `/tasks/<id>/delete/`      | task_delete       | Delete task (creator only)|
| `/admin/`                  | Django Admin      | Admin panel              |

---

## Role-Based Permission Summary

| Action              | Creator (Personal) | Assigner | Assignee |
|---------------------|--------------------|----------|----------|
| View task           | ✅                 | ✅       | ✅       |
| Edit title          | ✅                 | ❌       | ❌       |
| Edit description    | ✅                 | ❌       | ❌       |
| Edit priority       | ✅                 | ❌       | ❌       |
| Edit status         | ✅                 | ❌       | ✅       |
| Edit due date       | ✅                 | ✅       | ❌       |
| Delete task         | ✅                 | ❌       | ❌       |
| Assign to others    | ✅                 | —        | —        |

---

## Project Structure

```
taskflow/
├── manage.py
├── requirements.txt
├── README.md
├── taskmanager/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py      # Custom User model
│   ├── views.py       # Login, register, profile
│   ├── forms.py       # Auth forms
│   ├── urls.py
│   └── admin.py
├── tasks/
│   ├── models.py      # Task model
│   ├── views.py       # Dashboard, CRUD, permissions
│   ├── forms.py       # TaskForm, role-specific forms
│   ├── urls.py
│   └── admin.py
└── templates/
    ├── base.html
    ├── accounts/
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    └── tasks/
        ├── dashboard.html
        ├── task_form.html
        ├── task_detail.html
        ├── task_edit.html
        └── task_confirm_delete.html
```
