# Generated by Django 4.1.4 on 2022-12-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_reservation_supplements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='supplements',
        ),
        migrations.AddField(
            model_name='room',
            name='supplements',
            field=models.JSONField(default=None, null=True),
        ),
    ]