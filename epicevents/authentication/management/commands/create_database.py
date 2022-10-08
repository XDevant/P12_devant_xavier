from django.core.management.base import BaseCommand
from psycopg2.errors import ObjectInUse, OperationalError
from utils.utils import run_sql
from utils.prettyprints import PRR
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates database according to settings. USER needs to have Postgres credentials.'

    def add_arguments(self, parser):
        help_1 = 'Create an copy of the default db used as template for test db'
        parser.add_argument('-c', '--copy', action='store_true', help=help_1)

    def handle(self, *args, **options):
        name = settings.DATABASES['default']['NAME']
        if options['copy']:
            sql_1 = f'DROP DATABASE IF EXISTS "copy_{name}"'
            sql_2 = f'CREATE DATABASE "copy_{name}" TEMPLATE "{name}"'
            name = 'copy_' + name
        else:
            sql_1 = f'DROP DATABASE IF EXISTS "{name}"'
            sql_2 = f'CREATE DATABASE "{name}"'

        try:
            run_sql(sql_1)
            run_sql(sql_2)
            print(f"Database {PRR.colorize(name, True)} successfully created")
        except ObjectInUse:
            db = PRR.colorize(name, False)
            print(f"DB {db} already in use, make sure to quit pgAdmin")
        except OperationalError:
            db = PRR.colorize(name, False)
            print(f"Unable to connect to {db}, credentials are in config.py.")
        except Exception:
            db = PRR.colorize(name, False)
            print(f"Unable to create database {db}")
