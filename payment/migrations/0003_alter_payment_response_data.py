# Generated by Django 4.1.4 on 2022-12-19 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_amount_payment_subtotal_payment_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='response_data',
            field=models.JSONField(default=None, null=True),
        ),
    ]