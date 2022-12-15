from uuid import uuid4

from django.db import models

from payment.models import Payment

from hotel.models import Hotel

from traveler.models import Traveler


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='reservation_payments'
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE
    )
    search_parameters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservations'
        managed = True
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='reservation_rooms'
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservation_rooms'
        managed = True
        verbose_name = 'Reservation Rooms'
        verbose_name_plural = 'Reservation Rooms'


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    traveler = models.ForeignKey(
        Traveler,
        on_delete=models.CASCADE,
        related_name='guests'
    )
    is_lead = models.BooleanField()

    class Meta:
        db_table = 'guests'
        managed = True
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
