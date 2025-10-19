from django.contrib import admin
from .models import RoomTag, Room, Booking, USER_INFO_FIELDS
from .forms import BookingAdminForm


@admin.register(RoomTag)
class RoomTagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "responsible")
    filter_horizontal = ["tags"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(responsible=request.user)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm

    list_display = ['display_booking', 'applicant_name']
    list_filter = ("status", "room", "created_at")
    search_fields = ("applicant_name", "applicant_tg_username",
                     "applicant_tg_id", "applicant_phone", "event_name")
    search_help_text = (
        "Поиск по: имени заявителя, Telegram username/ID заявителя,"
        " телефону или названию мероприятия")
    ordering = ['-created_at', 'status']

    readonly_fields_for_all = ("applicant_tg_id", "created_at", "updated_at")

    fieldsets = (
        ("Информация от пользователя", {"fields": USER_INFO_FIELDS}),
        ("Общее", {"fields": ("status", "rejection_reason")}),
        ("Служебные поля", {"fields": readonly_fields_for_all}),
    )

    @admin.display(description="Бронирование")
    def display_booking(self, obj):
        if not obj.room:
            return "Без помещения"
        room_name = obj.room.title
        status = obj.get_status_display()
        start = obj.start_at.strftime("%d.%m.%Y %H:%M")
        return f"Бронь {room_name} с {start} ({status})"

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)

        class FormWithUser(Form):
            def __init__(self, *args, **kw):
                kw["user"] = request.user
                super().__init__(*args, **kw)

        return FormWithUser

    def get_readonly_fields(self, request, obj=None):
        ro = list(self.readonly_fields_for_all)
        if not request.user.is_superuser:
            ro += list(USER_INFO_FIELDS)
        return ro

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related("room")
        if request.user.is_superuser:
            return qs
        return qs.filter(room__responsible=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "room" and not request.user.is_superuser:
            kwargs["queryset"] = Room.objects.filter(responsible=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        return bool(obj.room and obj.room.responsible_id == request.user.id)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.is_staff
        return bool(obj.room and obj.room.responsible_id == request.user.id)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
