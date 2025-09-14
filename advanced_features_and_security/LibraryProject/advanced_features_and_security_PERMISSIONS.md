Permissions and Groups Setup

This project defines custom permissions on the `Book` model and provides a
management command to create user groups and assign permissions.

Custom permissions on `relationship_app.models.Book` (in `Meta.permissions`):
- can_view: Can view books
- can_create: Can create books
- can_edit: Can edit books
- can_delete: Can delete books

Legacy permissions are still present for backward compatibility: `can_add_book`, `can_change_book`, `can_delete_book`.

Setting up groups

Run the management command to create groups and attach permissions:

python manage.py setup_groups

This creates three groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

Enforcing permissions in views

`relationship_app/views.py` uses `@permission_required` decorators, for example:

@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    ...

Testing

- Create test users and assign them to the groups in the Django admin.
- Log in as each user and verify access control.

Notes about migrations

- After modifying `Meta.permissions`, run:

  python manage.py makemigrations
  python manage.py migrate

- Permissions are created as part of migrations; the management command assumes permissions exist.

If you'd like, I can:
- Add unit tests that create users/groups and assert view access control.
- Create an admin action or UI to manage default groups programmatically.
