from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from authentication.models import User, UserManager
from authentication.fixtures.fake_users import test_users
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'load 6 fake users for testing, 2 sales, 2 support, 1 admin, 1 without role'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for user in test_users:
            user["password"] = make_password(user["password"])
            User.objects.create(**user)
