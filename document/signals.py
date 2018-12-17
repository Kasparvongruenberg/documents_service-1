from django.db.models import signals
from django.dispatch import receiver

from .models import Document


@receiver(signals.pre_save, sender=Document)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()
