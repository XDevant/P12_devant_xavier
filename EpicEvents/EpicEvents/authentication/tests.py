from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


def create_test_users(apps, schema_migration):
    """Used in authentication.migrations.0002_auto... to create our test users"""
    user = get_user_model()

    user.objects.create(
        first_name="De",
        last_name="De",
        email="de@de.co",
        role="sales",
        password=make_password("mdp1")
    )
    user.objects.create(
        first_name="Do",
        last_name="Do",
        email="do@do.co",
        role="sales",
        password=make_password("mdp2")
    )
    user.objects.create(
        first_name="Bi",
        last_name="Bi",
        email="bi@bi.co",
        role="support",
        password=make_password("mdp3")
    )
    user.objects.create(
        first_name="Bo",
        last_name="Bo",
        email="bo@bo.co",
        role="support",
        password=make_password("mdp4")
    )
    user.objects.create(
      first_name="Za",
      last_name="Za",
      email="za@za.co",
      role="admin",
      password=make_password("mdp5")
    )
