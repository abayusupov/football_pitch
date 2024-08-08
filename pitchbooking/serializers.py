from rest_framework import serializers
from django.db import transaction
from .models import Contact, Address, Pitch, PitchImages, Booking
from authentication.models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name']

    full_name = serializers.CharField(source='get_full_name')



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchImages
        fields = ['image']


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitchImages
        fields = ['image']


class ListPitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'distance']

    distance = serializers.FloatField(read_only=True)



class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'distance', 'images']

    address = AddressSerializer()
    contact = ContactSerializer()
    images = ImageSerializer(many=True, read_only=True)
    distance = serializers.FloatField(read_only=True)




class MyPitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ['id', 'name', 'address', 'contact', 'price_per_hour', 'images']

    images = ImageSerializer(many=True)

    @transaction.atomic()
    def create(self, validated_data):
        images = validated_data.pop('images')
        user_id = self.context['user_id']
        owner = CustomUser.objects.get(id=user_id)
        pitch_instance = Pitch.objects.create(owner=owner, **validated_data)

        for image in images:
            image_instance = PitchImages.objects.create(**image)
            pitch_instance.images.add(image_instance.id)

        return pitch_instance




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pitch', 'start_time', 'end_time', 'client']

    client = CustomUserSerializer()

    def create(self, validated_data):
        user_id = self.context['user_id']
        client = CustomUser.objects.get(id=user_id)
        booking_instance = Booking.objects.create(client=client, **validated_data)
        return booking_instance


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pitch', 'start_time', 'end_time']

    def create(self, validated_data):
        user_id = self.context['user_id']
        client = CustomUser.objects.get(id=user_id)
        booking_instance = Booking.objects.create(client=client, **validated_data)
        return booking_instance