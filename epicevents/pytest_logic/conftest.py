import pytest
from rest_framework.test import APIClient
from django.db import connections
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase


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
    try:
        run_sql('CREATE DATABASE "copy_Epic-Events" TEMPLATE "Epic-Events"')
    except DuplicateDatabase:
        pass
    run_sql('CREATE DATABASE "test_Epic-Events" TEMPLATE "copy_Epic-Events"')

    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE IF EXISTS "test_Epic-Events"')


@pytest.fixture
def api_client():
    client = APIClient()
    return client
