from django.contrib import admin

from .models import RoomTag, Room


@admin.register(RoomTag)
class RoomTagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ["tags"]
