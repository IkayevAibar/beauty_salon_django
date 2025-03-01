# salon/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    
    path('specialists/', views.specialist_list, name='specialist_list'),
    path('specialists/<int:pk>/', views.specialist_detail, name='specialist_detail'),

    path('rating/<int:booking_id>/', views.add_rating, name='add_rating'),

    # Пример для страницы статистики
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('stats/', views.stats_view, name='stats'),
]
