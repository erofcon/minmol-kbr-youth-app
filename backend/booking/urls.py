from django.urls import path

from .views import RoomTagsView, RoomView, BookingView, RoomBusyView
from .views import BookingDetailView

urlpatterns = [
    path('room_tags/', RoomTagsView.as_view(), name='room-tags-list'),
    path('rooms/', RoomView.as_view(), name='room-list'),
    path('bookings/', BookingView.as_view(), name='booking-list-create'),
    path('rooms/<uuid:room_id>/busy/', RoomBusyView.as_view(),
         name='room-busy'),

    path('bookings/<uuid:pk>/', BookingDetailView.as_view(),
         name='booking-detail'),
]
