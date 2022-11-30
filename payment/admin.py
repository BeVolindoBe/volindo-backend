from django.contrib import admin

from payment.models import ReservationPayment, Reservation, Guest, Room


admin.site.register(ReservationPayment)
admin.site.register(Reservation)
admin.site.register(Guest)
admin.site.register(Room)
