from django.urls import path

from .views import RoomTagsView, RoomView, BookingView

urlpatterns = [
    path('room_tags/', RoomTagsView.as_view(), name='room-tags-list'),
    path('rooms/', RoomView.as_view(), name='room-list'),
    path('bookings/', BookingView.as_view(), name='booking-list-create'),
]
