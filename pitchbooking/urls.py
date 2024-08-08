from rest_framework import routers
from .views import AddressModelViewSet, PitchModelViewSet, ContactModelViewSet, MyBookedPitchesModelViewSet, MyPitchModelViewSet, BookingModelViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'addresses', AddressModelViewSet, basename='addresses')
router.register(r'contacts', ContactModelViewSet, basename='contacts')
router.register(r'pitches', PitchModelViewSet, basename='pitches')
router.register(r'my_bookings', MyBookedPitchesModelViewSet, basename='bookedpitches')
router.register(r'book_pitch', BookingModelViewSet, basename='bookpitch')
router.register(r'my_pitch', MyPitchModelViewSet, basename='mypitch')

urlpatterns = [
    path('', include(router.urls))
] 