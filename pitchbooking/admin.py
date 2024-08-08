from django.contrib import admin
from .models import Address, Contact, Pitch, PitchImages, Booking

# Register your models here.
admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Pitch)
admin.site.register(PitchImages)
admin.site.register(Booking)