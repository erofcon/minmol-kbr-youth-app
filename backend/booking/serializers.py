from rest_framework import serializers

from .models import RoomTag, Room, Booking


class RoomTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTag
        exclude = ['created_at', 'updated_at']


class RoomSerializer(serializers.ModelSerializer):
    tags = RoomTagSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.UUIDField(write_only=True, source='room')

    class Meta:
        model = Booking
        fields = [
            'id', 'room', 'room_id', 'status', 'start_at', 'end_at',
            'applicant_name', 'applicant_tg_username', 'applicant_phone',
            'event_name', 'event_purpose', 'target_audience',
            'invited_speakers', 'required_equipment',
            'rejection_reason', 'created_at'
        ]

        read_only_fields = ['id', 'status', 'rejection_reason', 'created_at']

    def create(self, validated_data):
        return super().create(validated_data)
