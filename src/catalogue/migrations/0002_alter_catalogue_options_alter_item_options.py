# Generated by Django 4.1.3 on 2022-11-17 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogue',
            options={'managed': True, 'ordering': ['description'], 'verbose_name': 'Catalogue', 'verbose_name_plural': 'Catalogues'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'managed': True, 'ordering': ['catalogue'], 'verbose_name': 'Catalogue item', 'verbose_name_plural': 'Catalogue items'},
        ),
    ]