from uuid import uuid4

from django.db import models


class Catalogue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    slug = models.CharField(max_length=40, db_index=True, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogues'
        managed = True
        verbose_name = 'Catalogue'
        verbose_name_plural = 'Catalogues'
        ordering = ['description']

    def __str__(self):
        return self.description


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE, related_name='items')
    slug = models.CharField(max_length=60, db_index=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'items'
        managed = True
        verbose_name = 'Catalogue item'
        verbose_name_plural = 'Catalogue items'
        ordering = ['catalogue']

    def __str__(self):
        if self.parent is None:
            return f'{self.description}'
        return f'{self.description} - {self.parent.description}'


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    iso_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'
        managed = True
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['iso_code']


class Destination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    destination = models.CharField(max_length=200)
    external_id = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'destinations'
        managed = True
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'
        ordering = ['destination']
