from uuid import uuid4

from django.db import models


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    country_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'countries'
        managed = True


class Destination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'destinations'
        managed = True
