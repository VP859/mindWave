# Generated by Django 5.1.1 on 2024-09-28 20:00

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("age", models.IntegerField(default=25)),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to=accounts.models.get_upload_path
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "role",
                    models.CharField(
                        choices=[("student", "Student"), ("teacher", "Teacher")],
                        default="student",
                        max_length=10,
                    ),
                ),
                ("points", models.IntegerField(default=0)),
                (
                    "rank",
                    models.CharField(
                        choices=[
                            ("IRON", "IRON"),
                            ("BRONZE", "BRONZE"),
                            ("SILVER", "SILVER"),
                            ("GOLD", "GOLD"),
                            ("PLATINUM", "PLATINUM"),
                            ("EMERALD", "EMERALD"),
                            ("DIAMOND", "DIAMOND"),
                        ],
                        default="IRON",
                        max_length=30,
                    ),
                ),
            ],
        ),
    ]
