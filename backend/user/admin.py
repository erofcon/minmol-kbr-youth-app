from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, GroupProxy


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'password2'),
        }),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name', 'phone', 'email'),
        }),

        ('Дополнительная информация', {
            'fields': ('telegram_id',),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительная информация', {'fields': ('telegram_id',)}),
    )


admin.site.unregister(Group)


@admin.register(GroupProxy)
class CustomGroupAdmin(GroupAdmin):
    pass
