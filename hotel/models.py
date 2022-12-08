from uuid import uuid4

from django.db import models

from catalogue.models import Destination, Item


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    destination = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='hotel_destination',
        null=True,
        default=None
    )
    provider = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='hotel_provider',
        null=True,
        default=None
    )
    external_id = models.CharField(max_length=100, db_index=True, null=True, default=None)
    hotel_name = models.CharField(max_length=200)
    stars = models.PositiveSmallIntegerField()
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    address = models.CharField(max_length=600, null=True, default=None)
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
    IMAGE_TYPE_CHOICES = (
        ('P', 'Principal'),
        ('A', 'Any'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='hotel_pictures'
    )
    image_type = models.CharField(max_length=1, choices=IMAGE_TYPE_CHOICES, default='A')
    url = models.URLField(max_length=600)

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
    amenity = models.CharField(max_length=100)

    class Meta:
        db_table = 'hotels_amenities'
        managed = True
        verbose_name = 'Hotel amenity'
        verbose_name_plural = 'Hotel amenities'
        ordering = ['hotel']

    def __str__(self):
        return f'{self.hotel.hotel_name}'
