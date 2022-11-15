# Generated by Django 4.1.3 on 2022-11-15 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_alter_item_metadata'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.ForeignKey(default='69e5e698-a900-4d14-a077-ba165f476a40', on_delete=django.db.models.deletion.DO_NOTHING, to='catalogue.item'),
        ),
    ]
