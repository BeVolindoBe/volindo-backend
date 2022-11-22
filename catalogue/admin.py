from django.contrib import admin

from catalogue.models import Catalogue, Item


class ItemAdmin(admin.ModelAdmin):
     list_display = [
        'catalogue',
        'description'
    ]


# admin.site.register(Catalogue)
# admin.site.register(Item, ItemAdmin)
