# Django Blog (AI Coder Edition)

This is a simple Django blog project created to follow the PRD for learning and demonstration purposes.

Features implemented:
- User registration, login, logout, profile edit
- Post CRUD (List/Detail/Create/Update/Delete) using CBVs
- Comment system: add/edit/delete comments (author-only edit/delete)
- Tagging using `django-taggit` and search with Q objects

Quick start

1. Create & activate a virtual environment (PowerShell example):

```powershell
python -m venv C:\path\to\venv
C:\path\to\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations and start server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

4. Open http://127.0.0.1:8000/ in your browser.

Notes
- The project currently uses Django's default User model. If you want a custom user model, do it early because it changes migrations.
- For email verification or production deployment, additional configuration is required.
