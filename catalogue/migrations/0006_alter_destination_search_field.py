# Generated by Django 4.1.4 on 2022-12-07 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_country_remove_item_metadata_remove_item_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='search_field',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
