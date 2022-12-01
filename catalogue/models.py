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
    parent = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE, related_name='items')
    slug = models.CharField(max_length=60, db_index=True, unique=True)
    description = models.CharField(max_length=100)
    metadata = models.JSONField(null=True)

    class Meta:
        db_table = 'items'
        managed = True
        verbose_name = 'Catalogue item'
        verbose_name_plural = 'Catalogue items'
        ordering = ['catalogue']

    def __str__(self):
        return self.description
