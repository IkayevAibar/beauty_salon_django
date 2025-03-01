# salon/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Specialist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='specialist_profile',
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    services = models.TextField(help_text="Перечислите услуги через запятую или опишите более детально.")
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.full_name


class Salon(models.Model):
    """
    Модель салона красоты (если предполагается несколько салонов).
    """
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    """
    Бронирование: пользователь записался к специалисту в определенный день и время.
    """
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
        ('finished', 'Завершено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='bookings')
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Дата и время, когда клиент хочет прийти
    date = models.DateField()
    time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.specialist.full_name} on {self.date} at {self.time}"


class Rating(models.Model):
    """
    Оценка за услугу. Связывается с конкретной записью (Booking).
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.booking}"
