from uuid import uuid4

from django.db import models

from agent.models import Agent


class ReservationPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approved_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self) -> str:
        return f'{self.agent.first_name} {self.agent.last_name}'


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    payment = models.ForeignKey(
        ReservationPayment,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    hotel_name = models.CharField(max_length=200)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservations'
        managed = True
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self) -> str:
        return f'{self.payment.agent.first_name} {self.payment.agent.first_name}'


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hotel = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='rooms')
    description = models.CharField(max_length=100, null=True, default=None)

    class Meta:
        db_table = 'rooms'
        managed = True
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self) -> str:
        return f'{self.hotel.agent.first_name} {self.hotel.agent.last_name}'


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_guests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'guests'
        managed = True
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
