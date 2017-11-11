from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MediaItem
from .tasks import scan_mediaitem


@receiver(post_save, sender=MediaItem, dispatch_uid="scan_media_item")
def scan_media_item(sender, instance, **kwargs):
    if instance.status == "received":
        scan_mediaitem.apply_async(args=[instance.id])

        instance.status = "scanning"
        instance.save()

    return instance
