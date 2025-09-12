Custom User Model (users_app.CustomUser)

This project uses a custom Django user model located at `users_app.models.CustomUser`.

Key fields added:
- `date_of_birth` (DateField)
- `profile_photo` (ImageField) — requires Pillow to handle image uploads

Settings:
- `AUTH_USER_MODEL = 'users_app.CustomUser'` is already set in `LibraryProject/settings.py`.

Development notes:
1. Install dependencies (in your virtualenv):

   pip install -r requirements.txt
   # or at minimum
   pip install Pillow

2. If you add or modify the model, create and apply migrations:

   python manage.py makemigrations
   python manage.py migrate

3. MEDIA settings (optional) — add to `LibraryProject/settings.py` if you want to serve uploaded files in development:

   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'

   And in `LibraryProject/urls.py` (development only):

   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
       # ...existing url patterns...
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

4. Creating a superuser (ensure email provided due to REQUIRED_FIELDS):

   python manage.py createsuperuser --username admin --email admin@example.com

If you'd like, I can add `requirements.txt`, MEDIA settings to `settings.py`, and a small test for the custom user manager.
