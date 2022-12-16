from uuid import uuid4

from django.db import models

from catalogue.models import Item

from agent.models import Agent


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='agent_payments'
    )
    payment_type = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approved_at = models.DateTimeField(null=True, default=None)
    response_data = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
