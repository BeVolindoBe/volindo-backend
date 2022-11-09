from uuid import uuid4

from django.db import models


class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    destination = models.IntegerField()
    check_in_date= models.DateField()
    number_of_rooms = models.PositiveIntegerField()
    number_of_adults = models.PositiveIntegerField()
    number_of_nights = models.PositiveIntegerField()
    number_of_child = models.PositiveIntegerField()
    hotel_info = models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hotels'
        managed = True
