# Generated by Django 4.1.3 on 2022-11-16 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveler',
            old_name='phone_contry_code',
            new_name='phone_country_code',
        ),
    ]
