# salon/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Базовые
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Услуги
    path('services/', views.services_list, name='services_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),

    # Бронирования
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/<int:service_id>/', views.booking_create, name='booking_create'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('bookings/<int:booking_id>/status/<str:new_status>/', views.booking_status_update, name='booking_status_update'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),

    # Отзывы
    path('booking/<int:booking_id>/rating/', views.add_rating, name='add_rating'),

    # Статистика
    path('stats/', views.stats_view, name='stats'),
]
