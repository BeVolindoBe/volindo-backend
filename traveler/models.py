from uuid import uuid4

from django.db import models

from catalogue.models import Item
from catalogue.constants import TITLE_CHOICES

from agent.models import Agent


class Traveler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='travelers')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    birthdate = models.DateField(null=True, default=None)
    age = models.IntegerField(null=True, default=None)
    phone_country_code = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='traveler_phone_contry_code',
        null=True,
        default=None
    )
    phone_number = models.CharField(max_length=10, null=True, default=None)
    title = models.CharField(max_length=2, choices=TITLE_CHOICES, null=True, default=None)
    traveler_status = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='traveler_status',
        default='ff82a0d3-7d21-4f8f-af9b-c28f61562749'
    )
    in_vacation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, default=None)
    country = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='traveler_country',
        null=True,
        default=None
    )
    city = models.CharField(max_length=200, null=True, default=None)
    state_province = models.CharField(max_length=200, null=True, default=None)
    zip_code = models.CharField(max_length=5, null=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'travelers'
        managed = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
