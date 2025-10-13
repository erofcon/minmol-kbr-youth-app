from rest_framework import generics

from .models import Center
from .serializers import CenterSerializer


class CenterListView(generics.ListAPIView):
    queryset = Center.objects.select_related('district').all()
    serializer_class = CenterSerializer
