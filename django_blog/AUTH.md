Authentication system for django_blog

Overview

This project uses Django's built-in authentication system with a small set of customizations:

- `RegistrationForm` extends `UserCreationForm` and adds an `email` field.
- Login and logout use Django's built-in class-based views (`LoginView`, `LogoutView`) with project templates located under `templates/registration/`.
- A simple `ProfileForm` allows users to edit `first_name`, `last_name`, and `email`.
- Views use `login_required` (function views) and `LoginRequiredMixin`/`UserPassesTestMixin` (class-based views) to protect actions.

Files of interest

- `blog/forms.py` - `RegistrationForm`, `ProfileForm` and `PostForm` (tags handling).
- `blog/views.py` - `register`, `profile`, and other blog-related views.
- `blog/urls.py` - authentication URL patterns: `/login/`, `/logout/`, `/register/`, `/profile/`.
- `templates/registration/` - templates for `login.html`, `logged_out.html`, `register.html`, and `profile.html`.

How registration works

1. The user visits `/register/`.
2. `register` view displays `RegistrationForm` (GET) or processes the form (POST).
3. On valid submission, the new user is created (password is handled via Django's secure hashing) and is logged in automatically with `login(request, user)`.
4. User is redirected to `LOGIN_REDIRECT_URL` (default: home page).

How login/logout works

- Login: `LoginView` is wired at `/login/`. On successful login, the user is redirected to `LOGIN_REDIRECT_URL`.
- Logout: `LogoutView` is wired at `/logout/` and uses `templates/registration/logged_out.html`.

Profile editing

- The `/profile/` view is protected by `login_required`.
- `ProfileForm` lets users update basic fields; a POST saves the changes and redirects back to the profile page.

Security notes

- All forms include CSRF tokens in templates.
- Passwords are stored using Django's built-in hashing and validators; no plain-text passwords are stored.
- Ensure `DEBUG = False` and `ALLOWED_HOSTS` are configured for production.

Testing the auth features

1. Run system checks and tests:

```powershell
. .\.venv\Scripts\Activate.ps1
python manage.py check
python manage.py test
```

2. Manual testing via the running dev server:

```powershell
. .\.venv\Scripts\Activate.ps1
python manage.py runserver
# open http://127.0.0.1:8000/register/ in a browser
```

Extending profiles

If you need more profile fields (avatar, bio), create a `Profile` model with a OneToOneField to `User`:

- Create `Profile` model in `blog.models` or a separate `accounts` app.
- Use signals (`post_save`) to create Profile instances automatically.
- Update `ProfileForm` to edit profile-specific fields and wire it into the `profile` view.

*** End of doc
