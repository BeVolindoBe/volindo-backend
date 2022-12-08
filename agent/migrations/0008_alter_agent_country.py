# Generated by Django 4.1.4 on 2022-12-08 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_alter_destination_search_field'),
        ('agent', '0007_alter_agent_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='country',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_country', to='catalogue.country'),
        ),
    ]