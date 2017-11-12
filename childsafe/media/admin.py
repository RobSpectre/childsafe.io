from django.contrib import admin

from .models import MediaItem
from .models import Match


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
