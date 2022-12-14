from uuid import uuid4

from django.db import models

from catalogue.models import Item

from payment.models import Payment

from hotel.models import Hotel

from traveler.models import Traveler


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='reservation_payment'
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE
    )
    reservation_status = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        default='39810fb8-7302-41aa-9939-e0d867513fd9' # pending
    )
    policies = models.JSONField(null=True, default=None)
    policies_acceptance = models.BooleanField(default=False)
    search_parameters = models.JSONField()
    booking_response = models.JSONField(null=True, default=None)
    booking_code = models.CharField(max_length=200, null=True, default=None)
    confirmation_number = models.CharField(max_length=200, null=True, default=None)
    cancelled_at = models.DateTimeField(null=True, default=None)
    cancellation_response = models.JSONField(null=True, default=None)
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
    name = models.CharField(max_length=200)
    supplements = models.JSONField(null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservation_rooms'
        managed = True
        verbose_name = 'Reservation Rooms'
        verbose_name_plural = 'Reservation Rooms'


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room_guests',
        null=True,
        default=None
    )
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
