# Generated by Django 4.1.3 on 2022-11-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_alter_hotelamenity_amenity_alter_hotelamenity_hotel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='adress',
            field=models.CharField(default=None, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
    ]
