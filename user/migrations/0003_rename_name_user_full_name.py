# Generated by Django 4.1.5 on 2023-01-09 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='full_name',
        ),
    ]
