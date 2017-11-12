import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ChildsafeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    email_address = models.EmailField()
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True)

    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    phone_notifications = models.BooleanField(default=False)

    def __str__(self):
        return "{0}: {1} {2}".format(self.id,
                                     self.first_name,
                                     self.last_name)
