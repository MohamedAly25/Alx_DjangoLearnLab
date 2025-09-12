from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom user manager that requires email and handles superuser flags."""

    use_in_migrations = True

"""
This app previously contained the CustomUser model. The model has been
moved to `bookshelf.models.CustomUser` and `AUTH_USER_MODEL` points there.

Keep this file present if other app-specific models are added here.
"""
    