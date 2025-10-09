from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, GroupProxy


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
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
        ('Персональные данные',
         {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительная информация', {'fields': ('telegram_id',)}),
    )


admin.site.unregister(Group)


@admin.register(GroupProxy)
class CustomGroupAdmin(GroupAdmin):
    pass


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Класс для отображения журнала изменений в админ-панели.
    """
    list_display = (
        'action_time',
        'user_link',
        'content_type',
        'object_link',
        'get_action_flag_display',
        'change_message',
    )

    list_filter = (
        'action_flag',
        'content_type',
        'user',
    )

    search_fields = (
        'object_repr',
        'change_message',
        'user__username',
    )

    ordering = ('-action_time',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Пользователь")
    def user_link(self, obj):
        """Ссылка на пользователя, совершившего действие."""
        user_url = reverse("admin:user_customuser_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', user_url, obj.user)

    @admin.display(description="Объект")
    def object_link(self, obj):
        """Ссылка на измененный объект (если он еще существует)."""
        try:
            url = reverse(
                f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change",
                args=[obj.object_id]
            )
            return format_html('<a href="{}">{}</a>', url, obj.object_repr)
        except NoReverseMatch:
            return obj.object_repr

    @admin.display(description="Действие")
    def get_action_flag_display(self, obj):
        """Цветное отображение типа действия."""
        actions = {
            1: ("Добавление", "green"),
            2: ("Изменение", "orange"),
            3: ("Удаление", "red"),
        }
        action, color = actions.get(obj.action_flag, ("Неизвестно", "black"))
        return format_html('<b style="color: {};">{}</b>', color, action)

    # --- Права доступа ---
    def has_module_permission(self, request):
        """Показываем этот раздел только суперпользователям."""
        return request.user.is_superuser
