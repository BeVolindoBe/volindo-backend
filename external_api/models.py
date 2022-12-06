from uuid import uuid4

from django.db import models

from catalogue.models import Item


class ExternalDestination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='provider')
    destination = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='destinations')
    external_id = models.CharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'external_destinations'
        managed = True

    def __str__(self):
        return f'{self.external_id}'
