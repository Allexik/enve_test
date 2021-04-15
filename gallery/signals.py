from django.core.files.storage import default_storage

from django.dispatch.dispatcher import receiver
from django.db.models import signals

from . import models


@receiver(signals.post_delete, sender=models.Photo)
def auto_delete_photo_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if default_storage.exists(instance.photo.path):
            default_storage.delete(instance.photo.path)


@receiver(signals.pre_save, sender=models.Photo)
def auto_delete_photo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_photo = models.Photo.objects.get(pk=instance.pk).photo
    except models.Photo.DoesNotExist:
        return False

    new_photo = instance.photo
    if not old_photo == new_photo:
        if default_storage.exists(old_photo.path):
            default_storage.delete(old_photo.path)
