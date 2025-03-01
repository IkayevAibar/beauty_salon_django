# salon/admin.py
from django.contrib import admin
from .models import Specialist, Salon, Booking, Rating

admin.site.register(Specialist)
admin.site.register(Salon)
admin.site.register(Booking)
admin.site.register(Rating)
