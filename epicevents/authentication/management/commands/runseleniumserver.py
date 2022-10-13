from django.core.management.commands.runserver import Command as BaseCommand
from django.core.management import call_command
from utils.utils import run_sql


class Command(BaseCommand):
    help = 'Runs a server with a copy of the test db as default.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from django.conf import settings
        name = settings.DATABASES['default']['NAME']
        name = name.split('_')[-1]
        settings.DATABASES['default']['NAME'] = f"selenium_{name}"
        run_sql(f'DROP DATABASE IF EXISTS "selenium_{name}"')
        run_sql(f'CREATE DATABASE "selenium_{name}" TEMPLATE "copy_{name}"')
        call_command('runserver', 7000)
