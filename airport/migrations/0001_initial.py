# Generated by Django 4.1.5 on 2023-01-09 10:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(db_index=True, default=None, max_length=100, null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_field', models.CharField(db_index=True, max_length=200)),
                ('destination', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airport_destination', to='catalogue.destination')),
                ('provider', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airport_provider', to='catalogue.item')),
            ],
            options={
                'verbose_name': 'Airport',
                'verbose_name_plural': 'Airports',
                'db_table': 'airports',
                'ordering': ['destination'],
                'managed': True,
            },
        ),
    ]
