from django.db import models

from catalogue.models import Item


class Log(models.Model):
    provider = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.URLField()
    payload = models.JSONField()
    status_code = models.PositiveSmallIntegerField()
    response = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'logs'
        managed = True
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
