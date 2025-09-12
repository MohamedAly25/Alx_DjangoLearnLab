from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
"""
Shim admin module: actual registration lives in `bookshelf.admin`.
Importing `bookshelf.admin` ensures the admin is registered when Django loads
this app's admin module.
"""

from bookshelf import admin as _bookshelf_admin  # noqa: F401
