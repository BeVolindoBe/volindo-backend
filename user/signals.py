from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User

from agent.models import Agent


@receiver(post_save, sender=User)
def user_signal(sender, instance, created, **kwargs):
    """
    When a new user registers, it creates an agent profile
    """
    if created:
        Agent.objects.create(
            user=instance,
            full_name=instance.full_name,
            email=instance.email
        )
