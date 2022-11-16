from django.contrib import admin

from catalogue.models import Item

from traveler.models import Traveler


class TravelerAdmin(admin.ModelAdmin):

    list_display = [
        'last_name',
        'first_name',
        'country',
        'agent'
    ]
    search_fields = ['last_name', 'first_name']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['traveler_status'].queryset = Item.objects.filter(
            catalogue__slug='traveler_status'
        )
        context['adminform'].form.fields['country'].queryset = Item.objects.filter(
            catalogue__slug='countries'
        )
        context['adminform'].form.fields['phone_country_code'].queryset = Item.objects.filter(
            catalogue__slug='phone_country_codes'
        )
        return super(TravelerAdmin, self).render_change_form(request, context, *args, **kwargs)

admin.site.register(Traveler, TravelerAdmin)
