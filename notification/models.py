from uuid import uuid4

from django.db import models

from agent.models import Agent


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('P', 'pop_up'),
        ('F', 'feed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=400)
    priority = models.PositiveSmallIntegerField(default=0)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPE_CHOICES)
    read = models.BooleanField(default=False)
    action = models.JSONField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        managed = True
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'

    def __str__(self) -> str:
        return f'{self.id}'
