from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book


class Command(BaseCommand):
    help = 'Create default groups (Viewers, Editors, Admins) and assign permissions for Book model'

    def handle(self, *args, **options):
        book_ct = ContentType.objects.get_for_model(Book)

        # Permission codenames (as defined in models.py)
        can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
        can_create = Permission.objects.get(codename='can_create', content_type=book_ct)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_ct)
        can_delete = Permission.objects.get(codename='can_delete', content_type=book_ct)

        viewers, _ = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.set([can_view])

        editors, _ = Group.objects.get_or_create(name='Editors')
        editors.permissions.set([can_view, can_create, can_edit])

        admins, _ = Group.objects.get_or_create(name='Admins')
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully'))
