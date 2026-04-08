# TaskFlow

A task management app I built with Django and PostgreSQL. Nothing fancy — just a clean way to create, assign, and track tasks with proper access control baked in.

---

## Stack

- **Backend:** Python 3.10+, Django 4.2
- **Frontend:** Django Templates + plain HTML/CSS/JS
- **Database:** PostgreSQL (configured via `dj-database-url`)
- **Auth:** Django's built-in session auth
- **Deployment:** Gunicorn + WhiteNoise for static files

---

## What it does

- Register, log in, log out, view your profile
- Create personal tasks or assign tasks to other users
- Task fields: title, description, status, priority, due date, assignee
- Dashboard with quick stats and filters by status, priority, and task type
- Access control — only the creator or assignee can open a task's detail page

### Permission rules

These are intentionally strict:

- **Creator, personal task** → can edit everything
- **Creator, assigned task** → can only change the due date
- **Assignee** → can only update the status
- **Delete** → creator only, always

---

## Getting started

### Prerequisites

- Python 3.10+
- PostgreSQL (local install or a hosted instance)
- `pip`

### 1. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Drop this in the project root and fill in your values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Recommended — just use a connection string
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME

# Fallback if DATABASE_URL isn't set
DB_NAME=taskmanager_db
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Seed some demo data

```bash
python manage.py seed_data
```

This sets up two test accounts you can use right away:
- `alice` / `Alice@1234`
- `bob` / `Bob@1234`

### 7. Start the dev server

```bash
python manage.py runserver
```

Head to `http://127.0.0.1:8000/` and you're in.

---

## URL reference

| URL | View |
|-----|------|
| `/` | `login_view` |
| `/login/` | `login_view` |
| `/register/` | `register_view` |
| `/logout/` | `logout_view` |
| `/profile/` | `profile_view` |
| `/dashboard/` | `dashboard` |
| `/tasks/create/` | `task_create` |
| `/tasks/<id>/` | `task_detail` |
| `/tasks/<id>/edit/` | `task_edit` |
| `/tasks/<id>/delete/` | `task_delete` |
| `/admin/` | Django admin |