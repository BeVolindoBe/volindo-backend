from uuid import uuid4

from django.db import models

from catalogue.models import Item


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_status = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        default='69e5e698-a900-4d14-a077-ba165f476a40'
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = True
