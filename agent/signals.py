from django.db.models.signals import post_save
from django.dispatch import receiver

from agent.models import Agent

from notification.models import Notification


@receiver(post_save, sender=Agent)
def agent_signal(sender, instance, created, **kwargs):
    """
    A welcome popup notification is created when the agent profile is created
    """
    if created:
        Notification.objects.create(
            agent=instance,
            title='Welcome to Volindo',
            message='Welcome to Volindo',
            notification_type='P'
        )
