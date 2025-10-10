from rest_framework import serializers

from .models import District, Center


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ['created_at', 'updated_at']


class CenterSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = Center
        exclude = ['created_at', 'updated_at']
