# salon/admin.py
from django.contrib import admin
from .models import Specialist, Service, Booking, Rating

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'experience_years')
    search_fields = ('full_name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'specialist')
    list_filter = ('specialist',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'service')
    search_fields = ('user__username', 'service__name')
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'comment')
    search_fields = ('booking__user__username', 'comment')
