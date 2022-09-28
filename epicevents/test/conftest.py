import pytest
from rest_framework.test import APIClient
from django.db import connections
from authentication.fixtures.fake_users import test_users, superuser
from utils.utils import run_sql


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings
    name = settings.DATABASES['default']['NAME']
    settings.DATABASES['default']['NAME'] = f"test_{name}"

    run_sql(f'DROP DATABASE IF EXISTS "test_{name}"')
    run_sql(f'CREATE DATABASE "test_{name}" TEMPLATE "copy_{name}"')

    yield

    for connection in connections.all():
        connection.close()

    run_sql(f'DROP DATABASE IF EXISTS "test_{name}"')


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

        def __init__(self, users, superuser):
            for user in users:
                if "role" in user.keys():
                    count = getattr(self, f'{user["role"]}_count')
                    setattr(self, f'{user["role"]}_{count}', {"email": user["email"], "password": user["password"]})
                    setattr(self, f'{user["role"]}_count', count + 1)
                else:
                    count = self.visitor_count
                    setattr(self, f'visitor_{count}', {"email": user["email"], "password": user["password"]})
                    self.visitor_count += 1

            self.superuser = {"email": superuser["email"], "password": superuser["password"]}

    return Logs(test_users, superuser)
