import pytest
from rest_framework.test import APIClient
from django.db import connections
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase
from authentication.fixtures.fake_users import test_users


def run_sql(sql):
    conn = psycopg2.connect(database="Epic-Events", user="postgres", password="supermdp")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'test_Epic-Events'

    run_sql('DROP DATABASE IF EXISTS "test_Epic-Events"')
    run_sql('CREATE DATABASE "test_Epic-Events" TEMPLATE "copy_Epic-Events"')

    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE IF EXISTS "test_Epic-Events"')


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def logins():
    """This fixture allows us to log our fake users during tests by passing **logins.role_n
    to client.login. The fake users need to be in the test bd.
    Since all tests need login and most log several users as parameter, the main goal is to provide
    better feedback with user parameter being named sales_3 instead of user_5"""
    class Logs:
        admin_count = 1
        sales_count = 1
        support_count = 1
        visitor_count = 1

        def __init__(self, users):
            for user in users:
                if "role" in user.keys():
                    count = getattr(self, f'{user["role"]}_count')
                    setattr(self, f'{user["role"]}_{count}', {"email": user["email"], "password": user["password"]})
                    setattr(self, f'{user["role"]}_count', count + 1)
                else:
                    count = self.visitor_count
                    setattr(self, f'visitor_{count}', {"email": user["email"], "password": user["password"]})
                    self.visitor_count += 1

    return Logs(test_users)
