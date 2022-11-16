from django.contrib import admin

from hotel.models import Hotel, HotelPicture, HotelAmenity


class HotelAdmin(admin.ModelAdmin):
    list_display = [
        'hotel_name',
        'destination',
        'stars'
    ]
    search_fields = ['hotel_name', ]


admin.site.register(HotelPicture)
admin.site.register(HotelAmenity)
admin.site.register(Hotel, HotelAdmin)
