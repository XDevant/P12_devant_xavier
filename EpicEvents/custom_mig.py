# Generated by Django 4.1 on 2022-08-10 18:02

from django.db import migrations
from EpicEvents.EpicEvents.authentication.groups import create_groups


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_groups)]