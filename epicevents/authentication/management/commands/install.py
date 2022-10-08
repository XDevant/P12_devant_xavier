from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections
from utils.errorlog import get_install_date, set_install_date


class Command(BaseCommand):
    help = 'Will chain the following manage.py commands to install the app after cloning: \
            makemigrations, create_database, migrate, create_groups, load_fake_users, \
           load_fake_data. Depending on the flags, fake data will be in test db only or both db.'

    def add_arguments(self, parser):
        help_1 = 'Fake items will be loaded in default db in addition to test db template'
        parser.add_argument('-f', '--fake', action='store_true', help=help_1)
        help_2 = 'Will create a superuser, logs are in fixture'
        parser.add_argument('-s', '--super', action='store_true', help=help_2)

    def handle(self, *args, **options):
        call_command('create_database')
        call_command('makemigrations')
        call_command('migrate')
        call_command('create_groups')
        if options['super']:
            call_command('load_fake_users', '--super')
        else:
            call_command('load_fake_users')
        if options['fake']:
            call_command('load_fake_items')
        for connection in connections.all():
            connection.close()
        call_command('create_database', '--copy')
        if not options['fake']:
            call_command('load_fake_items', '--copy')
        try:
            set_install_date()
            created = get_install_date()
        except OSError:
            created = None
        if created:
            print("An errors.log file has been successfully created in the base dir.")
        else:
            print("Unable to create errors.log")
