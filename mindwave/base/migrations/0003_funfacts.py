# Generated by Django 5.1.1 on 2024-09-29 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="FunFacts",
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
                ("fact", models.CharField(max_length=200)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="base.category"
                    ),
                ),
            ],
        ),
    ]
