from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.auth import TelegramInitDataAuthentication

from .models import Center
from .serializers import CenterSerializer


class CenterListView(generics.ListAPIView):
    queryset = Center.objects.select_related('district').all()
    serializer_class = CenterSerializer
    authentication_classes = [TelegramInitDataAuthentication]
    permission_classes = [IsAuthenticated]
