# Generated by Django 4.1.4 on 2022-12-19 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_reservation_policies_acceptance'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]