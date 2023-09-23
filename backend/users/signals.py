from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs): # noqa
    if created:
        instance.send_verify_email()
