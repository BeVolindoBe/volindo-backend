from uuid import uuid4

from django.db import models

from catalogue.models import Destination, Item


class Airport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='airport_destination',
        null=True,
        default=None
    )
    provider = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='airport_provider',
        null=True,
        default=None
    )
    external_id = models.CharField(max_length=100, db_index=True, null=True, default=None)
    airport_name = models.CharField(max_length=200)
    search_name = models.CharField(max_length=200, db_index=True)

    class Meta:
        db_table = 'airports'
        managed = True
        verbose_name = 'Airport'
        verbose_name_plural = 'Airports'
        ordering = ['destination']
