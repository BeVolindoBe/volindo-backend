from django.contrib import admin

from catalogue.models import Item

from hotel.models import Hotel, HotelPicture, HotelAmenity


class HotelAdmin(admin.ModelAdmin):
    list_display = [
        'hotel_name',
        'destination',
        'stars',
        'id'
    ]
    search_fields = ['hotel_name', ]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['destination'].queryset = Item.objects.filter(
            catalogue__slug='destinations'
        )
        return super(HotelAdmin, self).render_change_form(request, context, *args, **kwargs)



admin.site.register(HotelPicture)
admin.site.register(HotelAmenity)
admin.site.register(Hotel, HotelAdmin)
