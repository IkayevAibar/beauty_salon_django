# beauty_salon/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),  # все адреса приложения salon
]
