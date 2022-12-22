# Generated by Django 4.1.4 on 2022-12-22 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_country_metadata'),
        ('reservation', '0015_reservation_confirmation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_status',
            field=models.ForeignKey(default='39810fb8-7302-41aa-9939-e0d867513fd9', on_delete=django.db.models.deletion.CASCADE, to='catalogue.item'),
        ),
    ]
