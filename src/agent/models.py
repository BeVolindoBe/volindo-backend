from uuid import uuid4

from django.db import models

from catalogue.models import Item
from catalogue.constants import GENDER_CHOICES


class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField()
    country = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='agent_country'
    )
    phone_country_code = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='agent_phone_country_code'
    )
    phone_number = models.CharField(max_length=10)
    web_site = models.URLField()
    is_active = models.BooleanField(default=True)
    agent_status = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        default='69e5e698-a900-4d14-a077-ba165f476a40'
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agents'
        managed = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
