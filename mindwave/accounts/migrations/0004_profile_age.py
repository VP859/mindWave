# Generated by Django 5.1.1 on 2024-09-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_profile_teams"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="age",
            field=models.IntegerField(default=25),
        ),
    ]