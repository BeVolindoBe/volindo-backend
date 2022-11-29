from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from agent.models import Agent


@receiver(post_save, sender=User)
def user_signal(sender, instance, created, **kwargs):
    """
    When a new user registers, it creates an agent profile
    """
    if created:
        Agent.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )
