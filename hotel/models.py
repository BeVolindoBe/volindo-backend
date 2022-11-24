from uuid import uuid4

from django.db import models

from catalogue.models import Item


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    destination = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='hotel_destination'
    )
    hotel_name = models.CharField(max_length=200)
    stars = models.PositiveSmallIntegerField()
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    adress = models.CharField(max_length=600, null=True, default=None)
    description = models.TextField(null=True, default=None)

    class Meta:
        db_table = 'hotels'
        managed = True
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['destination']

    def __str__(self):
        return f'{self.hotel_name}'


class HotelPicture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='hotel_pictures'
    )
    url = models.URLField()

    class Meta:
        db_table = 'hotels_pictures'
        managed = True
        verbose_name = 'Hotel picture'
        verbose_name_plural = 'Hotel pictures'
        ordering = ['hotel']

    def __str__(self):
        return f'{self.hotel.hotel_name}'


class HotelAmenity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='hotel_amenities'
    )
    amenity = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'hotels_amenities'
        managed = True
        verbose_name = 'Hotel amenity'
        verbose_name_plural = 'Hotel amenities'
        ordering = ['hotel']

    def __str__(self):
        return f'{self.hotel.hotel_name}'