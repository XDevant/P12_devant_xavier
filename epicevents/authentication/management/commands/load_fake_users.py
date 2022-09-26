from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from authentication.models import User, UserManager
from authentication.fixtures.fake_users import test_users, superuser


class Command(BaseCommand):
    help = 'load 6 fake users for testing, 2 sales, 2 support, 1 admin, 1 without role'

    def add_arguments(self, parser):
        help_1 = 'Creates a superuser'
        parser.add_argument('-s', '--super', action='store_true', help=help_1)

    def handle(self, *args, **options):
        count = 0
        for user in test_users:
            user["password"] = make_password(user["password"])
            try:
                User.objects.create(**user)
                count += 1
            except IntegrityError:
                print(f"User {user['email']} already exists.")
        print(f"{count} users created")
        if options['super']:
            try:
                User.objects.create_superuser(**superuser)
                print("superuser created")
            except IntegrityError:
                print("superuser already exists.")
