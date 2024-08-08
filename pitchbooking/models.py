from django.db import models
from django.core.validators import RegexValidator
from authentication.models import CustomUser

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be entered in the format: '+998001234567'."
)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, validators=[phone_regex],)
    additional_phone_number1 = models.CharField(max_length=13, null=True, blank=True)
    additional_phone_number2 = models.CharField(max_length=13, null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.name



class PitchImages(models.Model):
    image = models.ImageField(upload_to='images/')
    # pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE, related_name='images')


class Pitch(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    contact = models.ForeignKey(Contact, on_delete=models.RESTRICT)
    price_per_hour = models.IntegerField()
    owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    images = models.ManyToManyField(PitchImages)

    def __str__(self) -> str:
        return self.name



class Booking(models.Model):
    pitch = models.ForeignKey(Pitch, on_delete=models.RESTRICT, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    client = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)



