from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Booking, Address, Contact, Pitch
from .serializers import AddressSerializer, PitchSerializer, ListPitchSerializer, MyPitchSerializer, ContactSerializer, CreateBookingSerializer, BookingSerializer
from django.db.models import FloatField, ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, ATan2, Sqrt
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPitchOwnerOrAdmin


class DistanceFunc:
    def __init__(self, lat1, lon1, lat2, lon2):
        lat1_rad = Radians(lat1)
        lon1_rad = Radians(lon1)
        lat2_rad = Radians(lat2)
        lon2_rad = Radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = Sin(dlat / 2) ** 2 + Cos(lat1_rad) * Cos(lat2_rad) * Sin(dlon / 2) ** 2
        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))

        self.distance = 6371.0 * c

    def __call__(self):
        return ExpressionWrapper(self.distance, output_field=FloatField())



class AddressModelViewSet(ModelViewSet):
    
    serializer_class = AddressSerializer
    permission_classes = [IsPitchOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_owner:
            return Address.objects.filter(owner_id=self.request.user.id)
        else:
            return Address.objects.all()


class ContactModelViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsPitchOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_owner:
            return Contact.objects.filter(owner_id=self.request.user.id)
        else:
            return Contact.objects.all()


class PitchModelViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pitch.objects.select_related('address', 'contact').prefetch_related('images', 'bookings').all()
    serializer_class = PitchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if lat and lon:
            lat = float(lat)
            lon = float(lon)
            distance_func = DistanceFunc(lat, lon, 'address__latitude', 'address__longitude')
            queryset = queryset.annotate(
                distance=distance_func()
            ).order_by('distance')

        
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        if start_time and end_time:
            queryset = queryset.exclude(
                bookings__start_time__lte=start_time, # booking_start <= start and booking_end >= end
                bookings__end_time__gte=end_time).exclude(
                                                   bookings__start_time__lte=start_time, # booking_start <= start < booking_end
                                                   bookings__end_time__gt=start_time).exclude(
                                                       bookings__start_time__lt=end_time, # booking_start < end <= booking_end
                                                       bookings__end_time__gte=end_time).exclude(
                                                           bookings__start_time__gte=start_time, # booking_start >= start and booking_end < end
                                                           bookings__end_time__lte=end_time
                                                       )
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ListPitchSerializer
        elif self.action == 'retrieve':
            return PitchSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        user_id = self.request.user.id
        return {'user_id': user_id}



class BookingModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    queryset = Booking.objects.all()
    serializer_class = CreateBookingSerializer

    def get_serializer_context(self):
        user_id = self.request.user.id
        return {'user_id': user_id}


class MyBookedPitchesModelViewSet(ModelViewSet):
    permission_classes = [IsPitchOwnerOrAdmin]
    http_method_names = ['get', 'delete']
    serializer_class = BookingSerializer
    

    def get_queryset(self):
        user_id = self.request.user.id
        return Booking.objects.select_related('pitch', 'client').filter(pitch__owner_id=user_id)


class MyPitchModelViewSet(ModelViewSet):
    permission_classes = [IsPitchOwnerOrAdmin]
    serializer_class = MyPitchSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Pitch.objects.filter(owner_id=user_id)






