# Generated by Django 4.1.4 on 2022-12-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_remove_room_policies_reservation_policies'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='policies_acceptance',
            field=models.BooleanField(default=False),
        ),
    ]