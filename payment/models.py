from uuid import uuid4

from django.db import models


class ExternalAgent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    external_id = models.CharField(max_length=40)
    agent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.URLField()
    agent_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'external_agents'
        managed = True
        verbose_name = 'External agent'
        verbose_name_plural = 'External agents'

    def __str__(self) -> str:
        return self.agent_name


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(
        ExternalAgent,
        on_delete=models.DO_NOTHING,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self) -> str:
        return self.agent.agent_name


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.DO_NOTHING,
        related_name='reservations'
    )
    hotel_name = models.CharField(max_length=200)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveSmallIntegerField()
    number_of_rooms = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservations'
        managed = True
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self) -> str:
        return self.agent.agent_name
