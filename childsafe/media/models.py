import uuid

from django.db import models

from web.models import ChildsafeUser


class MediaItem(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=255)
    url = models.URLField()
    status = models.CharField(max_length=255, default='received')

    scanned = models.BooleanField(default=False)

    user = models.ForeignKey(ChildsafeUser,
                             null=True,
                             related_name="mediaitems")

    def __str__(self):
        return "{0}: {1}".format(self.id, self.url)


class Match(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=255)
    url = models.URLField()

    risk = models.CharField(max_length=255)
    notified = models.BooleanField(default=False)

    user = models.ForeignKey(ChildsafeUser,
                             null=True,
                             related_name="matches")

    mediaitem = models.ForeignKey(MediaItem,
                                  null=True,
                                  related_name="matches")

    def __str__(self):
        return "{0}: {1} - {2}".format(self.id, self.risk, self.date_created)
