from uuid import uuid4

from django.db import models


class Catalog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    slug = models.CharField(max_length=40, db_index=True, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogs'
        managed = True


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    catalog = models.ForeignKey(Catalog, on_delete=models.DO_NOTHING, related_name='items')
    slug = models.CharField(max_length=40, db_index=True, unique=True)
    description = models.CharField(max_length=100)
    metadata = models.JSONField()

    class Meta:
        db_table = 'items'
        managed = True
