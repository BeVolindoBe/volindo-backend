from uuid import uuid4

from django.db import models


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    external_id = models.CharField(max_length=100, db_index=True, unique=True)
    hotel_name = models.CharField(max_length=40)
    star_rating = models.SmallPositiveIntegerField(default=0)
    hotel_description = models.CharField(max_length=2000)
    hotel_address = models.CharField(max_length=400)
    lat = models.DecimalField(max_digits=None, decimal_places=None, **options)
    lon = models.DecimalField(max_digits=None, decimal_places=None, **options)

    class Meta:
        db_table = 'hotels'
        managed = True
