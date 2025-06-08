# salon/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Specialist(models.Model):
    """
    Модель Specialist представляет специалиста в салоне красоты.
    Атрибуты:
        user (OneToOneField): Связь один-к-одному с моделью User, представляющая пользователя, связанного с этим специалистом.
        full_name (CharField): Полное имя специалиста, ограниченное 100 символами.
        experience_years (PositiveIntegerField): Количество лет опыта работы специалиста.
        bio (TextField): Биография специалиста, может быть пустой.
    Методы:
        __str__(): Возвращает строковое представление полного имени специалиста.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='specialist_profile',
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='specialists/', null=True, blank=True)

    @property
    def average_rating(self):
        avg = Rating.objects.filter(booking__service__specialist=self).aggregate(
            avg=Avg('rating')
        )['avg']
        return avg or 0
    
    @property
    def reviews(self):
        return Rating.objects.filter(booking__service__specialist=self).select_related('booking', 'booking__user')
    
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"
        ordering = ['full_name']
        unique_together = ('user', 'full_name')


class Service(models.Model):
    """
    Модель, представляющая услугу в салоне красоты.
    Атрибуты:
        name (CharField): Название услуги, ограниченное 100 символами.
        description (TextField): Описание услуги, может быть пустым.
        price (DecimalField): Цена услуги с максимальной длиной 8 цифр и 2 десятичными знаками.
        specialist (ForeignKey): Ссылка на специалиста, предоставляющего услугу, с каскадным удалением и обратной связью 'services'.
    Методы:
        __str__(): Возвращает строковое представление услуги (название).
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='services')
    photo = models.FileField("Картинка услуги", upload_to="files/", null=True, blank=True)
    duration_minutes = models.PositiveIntegerField("Длительность (мин)", default=60)
    details = models.TextField("Что входит в услугу", blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']
        unique_together = ('name', 'specialist')


class Booking(models.Model):
    """
    Бронирование: пользователь записался на услугу в определенный день и время.

    Атрибуты:
        user (ForeignKey): Пользователь, который сделал бронирование.
        service (ForeignKey): Услуга, на которую записался пользователь.
        date (DateField): Дата, когда клиент хочет прийти.
        time (TimeField): Время, когда клиент хочет прийти.
        status (CharField): Статус бронирования (ожидает подтверждения, подтверждено, отменено, завершено).
        created_at (DateTimeField): Дата и время создания бронирования.
    Методы:
        __str__: Возвращает строковое представление бронирования.
    """
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
        ('finished', 'Завершено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    
    # Дата и время, когда клиент хочет прийти
    date = models.DateField()
    time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.service.name}({self.service.specialist.full_name}) на {self.date} в {self.time}"
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-created_at']
        unique_together = ('user', 'service', 'date', 'time')


class Rating(models.Model):
    """
    Оценка за услугу. Связывается с конкретной записью (Booking).
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.booking}"
    
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-booking__created_at']
