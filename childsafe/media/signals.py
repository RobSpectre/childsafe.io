from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MediaItem
from .models import Match

from .tasks import scan_mediaitem
from .tasks import notify_match


@receiver(post_save, sender=MediaItem, dispatch_uid="scan_media_item")
def scan_media_item(sender, instance, **kwargs):
    if not instance.scanned:
        scan_mediaitem.apply_async(args=[instance.id])

        instance.scanned = True
        instance.save()

    return instance


@receiver(post_save, sender=Match, dispatch_uid="notify_match")
def initiate_notify_match(sender, instance, **kwargs):
    if not instance.notified:
        notify_match.apply_async(args=[instance.id])

        instance.notified = True
        instance.save()

    return instance
