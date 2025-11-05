from rest_framework import serializers
from core.utils import AbsoluteHTTPSImageField
from .models import District, Center


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ['created_at', 'updated_at']


class CenterSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    emblem = AbsoluteHTTPSImageField(allow_null=True, required=False)

    class Meta:
        model = Center
        exclude = ['created_at', 'updated_at']
