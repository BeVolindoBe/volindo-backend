from django.contrib import admin

from hotel.models import Hotel, HotelPicture, HotelAmenity


admin.site.register(HotelPicture)
admin.site.register(HotelAmenity)
admin.site.register(Hotel)