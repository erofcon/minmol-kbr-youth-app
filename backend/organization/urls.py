from django.urls import path

from .views import CenterListView

urlpatterns = [
    path('centers/', CenterListView.as_view(), name='center-list'),
]
