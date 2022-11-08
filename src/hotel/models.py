from uuid import uuid4

from django.db import models


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hotel_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'hotels'
        managed = True
