# Generated by Django 4.1.4 on 2022-12-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traveler', '0009_remove_traveler_age_alter_traveler_traveler_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveler',
            name='phone_country_code',
            field=models.CharField(default=None, max_length=5, null=True),
        ),
    ]