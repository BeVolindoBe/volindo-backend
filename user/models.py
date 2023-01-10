from uuid import uuid4

from django.db import models

from catalogue.models import Country


class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    external_id = models.UUIDField(db_index=True, editable=False, default=None)
    full_name = models.CharField(max_length=200, default=None)
    email = models.EmailField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = True

    def __str__(self):
        return f'{self.full_name}'
