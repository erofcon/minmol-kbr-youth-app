from rest_framework import serializers

from event.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_at', 'updated_at']