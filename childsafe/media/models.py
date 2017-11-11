import uuid

from django.db import models


class MediaItem(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_id = models.CharField(max_length=255)
    url = models.URLField()
    status = models.CharField(max_length=255, default='received')

    scanned = models.BooleanField(default=False)
    positive = models.BooleanField(default=False)
    alerted = models.BooleanField(default=False)

    def __str__(self):
        return "{0}: {1}".format(self.id, self.url)
