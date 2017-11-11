from django.contrib import admin

from .models import ChildsafeUser 


@admin.register(ChildsafeUser)
class ChildsafeUserAdmin(admin.ModelAdmin):
    pass
