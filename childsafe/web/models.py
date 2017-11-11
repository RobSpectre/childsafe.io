import uuid

from django.contrib.auth.models import User
from django.db import models


class ChildsafeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    email_address = models.EmailField()
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True)
