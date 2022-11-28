# Generated by Django 4.1.3 on 2022-11-27 20:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.CharField(db_index=True, max_length=40, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Catalogue',
                'verbose_name_plural': 'Catalogues',
                'db_table': 'catalogues',
                'ordering': ['description'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.CharField(db_index=True, max_length=60, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('metadata', models.JSONField(null=True)),
                ('catalogue', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='catalogue.catalogue')),
            ],
            options={
                'verbose_name': 'Catalogue item',
                'verbose_name_plural': 'Catalogue items',
                'db_table': 'items',
                'ordering': ['catalogue'],
                'managed': True,
            },
        ),
    ]
