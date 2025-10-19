from rest_framework import serializers
from organization.serializers import CenterSerializer

from .models import RoomTag, Room, Booking, Status


class RoomTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTag
        exclude = ['created_at', 'updated_at']


class RoomSerializer(serializers.ModelSerializer):
    tags = RoomTagSerializer(read_only=True, many=True)
    center = CenterSerializer(read_only=True)

    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.filter(is_active=True),
        write_only=True,
        source='room',
        pk_field=serializers.UUIDField()
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'room', 'room_id', 'status', 'start_at', 'end_at',
            'applicant_name', 'applicant_tg_id', 'applicant_tg_username',
            'applicant_phone',
            'event_name', 'event_purpose', 'target_audience',
            'invited_speakers', 'required_equipment',
            'rejection_reason', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'rejection_reason', 'created_at',
                            'applicant_tg_id', 'applicant_tg_username']

    def validate(self, attrs):
        room = attrs.get('room') or getattr(self.instance, 'room', None)
        start_at = attrs.get('start_at') or getattr(self.instance, 'start_at',
                                                    None)
        end_at = attrs.get('end_at') or getattr(self.instance, 'end_at', None)

        if start_at and end_at and room:
            if end_at <= start_at:
                raise serializers.ValidationError({
                    'end_at': 'Окончание бронирования должно быть позже начала.'})

            qs = Booking.objects.filter(
                room=room,
                status__in=[Status.APPROVED],
                start_at__lt=end_at,
                end_at__gt=start_at,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    'В выбранный период помещение уже занято.')

        return attrs


class BookingBusySerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('start_at', 'end_at')
