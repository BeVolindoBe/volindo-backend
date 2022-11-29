# Generated by Django 4.1.3 on 2022-11-29 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_alter_item_catalogue'),
        ('agent', '0004_alter_agent_agent_status_alter_agent_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='agent_subscription',
            field=models.ForeignKey(default='5d7b286e-cab3-4869-b420-119f9bd8b2e9', on_delete=django.db.models.deletion.CASCADE, related_name='agent_subscription', to='catalogue.item'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='agent_status',
            field=models.ForeignKey(default='69e5e698-a900-4d14-a077-ba165f476a40', on_delete=django.db.models.deletion.CASCADE, related_name='agent_status', to='catalogue.item'),
        ),
    ]
