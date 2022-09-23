from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from authentication.fixtures.groups import groups


class Command(BaseCommand):
    help = 'creates "sales", "support, "admin" and "visitor" groups and gives them permissions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for key, value in groups.items():
            group = Group(name=key)
            group.save()
            for model, perm_list in value.items():
                for perm in perm_list:
                    group.permissions.add(Permission.objects.get(codename=f"{perm}_{model}"))
