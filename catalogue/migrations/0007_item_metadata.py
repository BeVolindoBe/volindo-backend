# Generated by Django 4.1.4 on 2022-12-14 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_alter_destination_search_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='metadata',
            field=models.JSONField(default=None, null=True),
        ),
    ]