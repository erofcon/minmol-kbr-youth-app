from django.contrib import admin
from .models import District, Center


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Center)
class CentersAdmin(admin.ModelAdmin):
    list_display = ["name"]
