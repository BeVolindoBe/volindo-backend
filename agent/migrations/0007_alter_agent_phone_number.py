# Generated by Django 4.1.3 on 2022-11-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0006_alter_agent_agent_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='phone_number',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]