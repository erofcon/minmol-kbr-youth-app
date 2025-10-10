from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .models import Center
from .serializers import CenterSerializer


class CenterListView(generics.ListAPIView):
    queryset = Center.objects.select_related('district').all()
    serializer_class = CenterSerializer

    # def get(self, request, *args, **kwargs):
    #     centers = Center.objects.select_related('district').all()
    #     serializer = CenterSerializer(centers, many=True)
    #     return Response(serializer.data)
