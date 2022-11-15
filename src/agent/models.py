from uuid import uuid4

from django.db import models

from user.models.import User

from catalogue.models import Item


class Agent(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Non binary'),
        ('O', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField()
    phone_contry_code = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    phone number = models.CharField(max_length=10)
    webpage = models.URLField()
    country = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agents'
        managed = True
