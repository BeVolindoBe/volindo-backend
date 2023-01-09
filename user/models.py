from uuid import uuid4

from django.db import models

from catalogue.models import Country


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = models.CharField(max_length=200, default=None)
    email = models.EmailField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return f'{self.full_name}'
