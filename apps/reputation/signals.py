# apps/reputation/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .services import award_rep

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_signup(sender, instance, created, **kwargs):
    if created:
        award_rep(instance, 'SIGNUP_BONUS')