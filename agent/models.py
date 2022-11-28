from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from catalogue.models import Item


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, default=None)
    country = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='agent_country',
        null=True,
        default=None
    )
    phone_country_code = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='agent_phone_country_code',
        null=True,
        default=None
    )
    phone_number = models.CharField(max_length=10, null=True, default=None)
    web_site = models.URLField(null=True, default=None)
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
