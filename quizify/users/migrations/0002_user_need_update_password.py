# Generated by Django 5.0.10 on 2025-01-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="need_update_password",
            field=models.BooleanField(
                default=False, verbose_name="Need update password"
            ),
        ),
    ]
