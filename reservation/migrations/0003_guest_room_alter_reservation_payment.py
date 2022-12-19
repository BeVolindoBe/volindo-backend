# Generated by Django 4.1.4 on 2022-12-15 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_amount_payment_subtotal_payment_payment_type'),
        ('reservation', '0002_reservation_booking_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_guests', to='reservation.room'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_payment', to='payment.payment'),
        ),
    ]