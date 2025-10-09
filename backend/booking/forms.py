from django import forms
from django.utils.safestring import mark_safe

from .models import Booking, Status


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields["status"].widget = forms.RadioSelect(
            choices=self.fields["status"].choices
        )

        if user and not user.is_superuser:
            allowed = [
                (Status.APPROVED, Status.APPROVED.label),
                (Status.REJECTED, Status.REJECTED.label),
            ]

            # показываем текущий статус
            if self.instance and self.instance.pk:
                self.fields["status"].help_text = mark_safe(
                    f"<strong>Текущий статус: {self.instance.get_status_display()}</strong>"
                )

            instance_status = getattr(self.instance, "status", None)
            allowed_values = {v for v, _ in allowed}
            if instance_status not in allowed_values:

                self.fields["status"].choices = allowed
                self.initial["status"] = ""
            else:
                self.fields["status"].choices = allowed

            self.fields["status"].label = "Выберите действие"

    def clean_status(self):
        value = self.cleaned_data.get("status")
        user = self.user
        if user and not user.is_superuser:
            if value in (None, ""):
                raise forms.ValidationError("Выберите действие.")
            if value not in (Status.APPROVED, Status.REJECTED):
                raise forms.ValidationError(
                    "Недопустимый статус для вашей роли.")
        return value
