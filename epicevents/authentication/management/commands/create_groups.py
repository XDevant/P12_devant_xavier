from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from authentication.fixtures.groups import groups
from utils.prettyprints import PRR


class Command(BaseCommand):
    help = 'creates "sales", "support, "admin" and "visitor" groups and gives them permissions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        oks = []
        kos = []
        for key, value in groups.items():
            kos = []
            try:
                group = Group(name=key)
                group.save()
            except Exception:
                ko = key.title()
                ko = PRR.colorize(ko.strip(', '), False)
                print(f"Something went wrong while creating group {ko}.")
                continue
            for model, perm_list in value.items():
                for perm in perm_list:
                    try:
                        name = f"{perm}_{model}"
                        perm = Permission.objects.get(codename=name)
                        group.permissions.add(perm)
                    except Exception:
                        kos.append(name)
            if len(kos) == 0:
                ok = PRR.colorize(key.title(), True)
                print(f"Group {ok} have been successfully created.")
            else:
                ok = PRR.colorize(key.title(), False)
                ko = ', '.join(kos)
                ko = PRR.colorize(ko, False)
                msg = "Something went wrong while enabling permission(s)"
                print(f"{msg} {ko} for group{ok}.")
