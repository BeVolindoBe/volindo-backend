from uuid import uuid4

from django.db import models

from catalogue.models import Item
from catalogue.constants import GENDER_CHOICES

from agent.models import Agent


class Traveler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, related_name='travelers')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    birthdate = models.DateField()
    phone_contry_code = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='traveler_phone_contry_code'
    )
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    traveler_status = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='traveler_status'
    )
    in_vacation = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    country = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='traveler_country'
    )
    city = models.CharField(max_length=200)
    state_province = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=5)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'travelers'
        managed = True
