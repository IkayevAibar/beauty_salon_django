# salon/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from .models import Specialist, Service, Booking, Rating
from .forms import (
    BookingEditForm,
    RegistrationForm,
    ServiceForm,
    BookingForm,
    RatingForm,
)

from datetime import date, timedelta
from django.db.models import Avg, Count
# ----------------------------------------------------------
# Вспомогательные проверки / декораторы
# ----------------------------------------------------------

def is_admin(user):
    return user.is_staff  # или другая логика


def is_specialist(user):
    # Если пользователь связан со Specialist, считаем его специалистом
    return hasattr(user, 'specialist_profile')


# ----------------------------------------------------------
# Базовые вьюхи (регистрация/логин/логаут)
# ----------------------------------------------------------
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'salon/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверные логин или пароль")
    return render(request, 'salon/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


# ----------------------------------------------------------
# Главная страница
# ----------------------------------------------------------
def home(request):
    services = Service.objects.all()[:4]

    # Пример: соберём данные на неделю вперёд (7 дней),
    # считаем, сколько бронирований на каждый день
    # Это базовый вариант, доработайте логику по вкусу
    import datetime
    today = datetime.date.today()
    schedule = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        count = Booking.objects.filter(date=day).count()
        # Собираем словари
        schedule.append({
            'date': day.strftime('%d-%m-%Y'),
            'bookings_count': count
        })

    # Передаём schedule в контекст
    return render(request, 'salon/home.html', {
        'services': services,
        'schedule': schedule,
    })


# ----------------------------------------------------------
# Просмотр и управление услугами (Service)
# ----------------------------------------------------------

@login_required
@user_passes_test(is_admin)
def service_create(request):
    # Доступно только админам
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Услуга успешно создана.")
            return redirect('services_list')
    else:
        form = ServiceForm()
    return render(request, 'salon/service_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def service_edit(request, service_id):
    # Редактировать услугу может только админ
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Услуга обновлена.")
            return redirect('services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'salon/service_form.html', {'form': form, 'service': service})


@login_required
@user_passes_test(is_admin)
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, "Услуга удалена.")
    return redirect('services_list')


def services_list(request):
    # Доступно для всех (просто просмотр)
    services = Service.objects.annotate(
        average_rating=Avg('bookings__rating__rating'),
        ratings_count=Count('bookings__rating')
    )
    return render(request, 'salon/services_list.html', {'services': services})


def service_detail(request, service_id):
    # Детальная страница услуги
    
    service = get_object_or_404(Service.objects.annotate(
        average_rating=Avg('bookings__rating__rating'),
        ratings_count=Count('bookings__rating'),
    ).select_related('specialist'),  # Добавьте эту строку
        id=service_id
    )

    # Получаем другие услуги специалиста (исключая текущую)
    other_services = service.specialist.services.exclude(id=service.id)[:4]

    # По умолчанию считаем, что пользователь не записан
    is_already_booked = False

    ratings = Rating.objects.filter(booking__service=service).select_related('booking__user')

    if request.user.is_authenticated:
        # Ищем бронирования этого пользователя для текущей услуги
        # Например, статус 'pending' или 'confirmed' (ещё не отменённые / не завершённые)
        qs = Booking.objects.filter(
            user=request.user,
            service=service,
            status__in=['pending', 'confirmed']  # вы можете расширить логику
        )
        if qs.exists():
            is_already_booked = True

    return render(request, 'salon/service_detail.html', {
        'service': service,
        'ratings': ratings,
        'is_already_booked': is_already_booked,
        'other_services': other_services
    })


# ----------------------------------------------------------
# Бронирования (Booking)
# ----------------------------------------------------------
@login_required
def booking_create(request, service_id):
    # Пользователь хочет записаться на конкретную услугу
    service = get_object_or_404(Service, id=service_id)

    if request.user.is_staff or hasattr(request.user, 'specialist_profile'):
        messages.error(request, "Специалистам и администраторам нельзя создавать запись на себя.")
        return redirect('services_list')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, "Вы успешно записались!")
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'salon/booking_create.html', {
        'form': form,
        'service': service
    })


@login_required
def booking_list(request):
    # Если пользователь - админ, но не специалист
    if request.user.is_staff and not hasattr(request.user, 'specialist_profile'):
        # видит все
        bookings = Booking.objects.select_related('service', 'user').all()
    # Иначе, если специалист (возможно, он же staff)
    elif is_specialist(request.user):
        specialist = request.user.specialist_profile
        bookings = Booking.objects.filter(service__specialist=specialist)
    else:
        # обычный пользователь
        bookings = Booking.objects.filter(user=request.user)
    
    return render(request, 'salon/booking_list.html', {'bookings': bookings})



@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # проверяем права
    if request.user.is_staff:
        # админ видит всё
        pass
    elif is_specialist(request.user):
        # специалист видит только, если booking принадлежит к его услугам
        if booking.service.specialist != request.user.specialist_profile:
            messages.error(request, "У вас нет доступа к этому бронированию.")
            return redirect('booking_list')
    else:
        # обычный пользователь может просматривать только свои
        if booking.user != request.user:
            messages.error(request, "У вас нет доступа к этому бронированию.")
            return redirect('booking_list')

    return render(request, 'salon/booking_detail.html', {'booking': booking})

@login_required
def booking_status_update(request, booking_id, new_status):
    """
    Позволяет администратору или специалисту обновить статус бронирования.
    new_status может быть: 'pending', 'confirmed', 'finished', 'canceled', etc.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    # Проверка прав:
    # 1) Если user.is_staff (админ), может менять любой статус
    # 2) Если это специалист, то только для своих услуг
    if request.user.is_staff:
        pass  # разрешаем
    elif hasattr(request.user, 'specialist_profile'):
        # Специалист может изменить только, если это запись на его услугу
        if booking.service.specialist != request.user.specialist_profile:
            messages.error(request, "Вы не можете менять статус чужого бронирования.")
            return redirect('booking_list')
    else:
        messages.error(request, "У вас нет прав менять статус бронирования.")
        return redirect('booking_list')

    # Проверяем, что new_status в допустимых значениях:
    valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]  
    if new_status not in valid_statuses:
        messages.error(request, f"Недопустимый статус: {new_status}")
        return redirect('booking_list')

    # Обновляем статус
    booking.status = new_status
    booking.save()
    messages.success(request, f"Статус бронирования #{booking.id} изменён на {booking.get_status_display()}.")
    return redirect('booking_list')


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # те же проверки, что выше
    if not request.user.is_staff and not is_specialist(request.user) and booking.user != request.user:
        messages.error(request, "У вас нет прав отменять это бронирование.")
        return redirect('booking_list')

    booking.status = 'canceled'
    booking.save()
    messages.success(request, "Бронирование отменено.")
    return redirect('booking_list')


@login_required
def booking_edit(request, booking_id):
    """
    Редактирование даты/времени бронирования (админ может редактировать всё,
    пользователь — только свою запись, специалист — только если запись на его услугу).
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование обновлено.")
            return redirect('booking_list')
    else:
        # Важно: при GET-запросе передаём instance=booking
        form = BookingEditForm(instance=booking)

    return render(request, 'salon/booking_edit.html', {
        'form': form,
        'booking': booking
    })


# ----------------------------------------------------------
# Отзывы (Rating)
# ----------------------------------------------------------

@login_required
def add_rating(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # проверяем, что пользователь владеет бронированием
    if booking.user != request.user and not request.user.is_staff:
        messages.error(request, "У вас нет прав оставлять отзыв на чужое бронирование.")
        return redirect('booking_list')

    # проверяем, что бронирование не отменено
    if booking.status not in ['finished', 'confirmed']:
        messages.error(request, "Нельзя оставить отзыв для незавершённой или отменённой записи.")
        return redirect('booking_list')

    # если уже есть рейтинг, возможно, редактируем?
    rating_obj = getattr(booking, 'rating', None)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating_obj)
        if form.is_valid():
            rating_to_save = form.save(commit=False)
            rating_to_save.booking = booking
            rating_to_save.save()
            messages.success(request, "Спасибо за ваш отзыв!")
            return redirect('booking_list')
    else:
        form = RatingForm(instance=rating_obj)

    return render(request, 'salon/rating_form.html', {
        'form': form,
        'booking': booking
    })


# ----------------------------------------------------------
# Статистика (Admin / Specialist)
# ----------------------------------------------------------

@login_required
def stats_view(request):
    today = date.today()
    schedule = []
    for i in range(7):
        day = today + timedelta(days=i)
        if request.user.is_staff:
            count = Booking.objects.filter(date=day).count()
        elif is_specialist(request.user):
            specialist = request.user.specialist_profile
            count = Booking.objects.filter(date=day, service__specialist=specialist).count()
        else:
            count = 0
        schedule.append({
            'date': day.strftime('%d-%m-%Y'),
            'bookings_count': count
        })

    if request.user.is_staff:
        total_bookings = Booking.objects.count()
        finished_bookings = Booking.objects.filter(status='finished').count()
        canceled_bookings = Booking.objects.filter(status='canceled').count()
        all_ratings = Rating.objects.all()
        avg_rating = sum(r.rating for r in all_ratings) / all_ratings.count() if all_ratings else 0

        context = {
            'total_bookings': total_bookings,
            'finished_bookings': finished_bookings,
            'canceled_bookings': canceled_bookings,
            'avg_rating': avg_rating,
            'schedule': schedule,
        }
        return render(request, 'salon/admin_stats.html', context)

    elif is_specialist(request.user):
        specialist = request.user.specialist_profile
        my_bookings = Booking.objects.filter(service__specialist=specialist)
        total_bookings = my_bookings.count()
        finished_bookings = my_bookings.filter(status='finished').count()
        canceled_bookings = my_bookings.filter(status='canceled').count()
        all_ratings = Rating.objects.filter(booking__service__specialist=specialist)
        avg_rating = sum(r.rating for r in all_ratings) / all_ratings.count() if all_ratings else 0

        context = {
            'total_bookings': total_bookings,
            'finished_bookings': finished_bookings,
            'canceled_bookings': canceled_bookings,
            'avg_rating': avg_rating,
            'schedule': schedule,
        }
        return render(request, 'salon/master_stats.html', context)

    messages.error(request, "У вас нет доступа к статистике.")
    return redirect('home')

# ----------------------------------------------------------
# Специалисты (Specialist)
# ----------------------------------------------------------

def specialist_detail(request, pk):
    specialist = get_object_or_404(Specialist, pk=pk)
    return render(request, 'salon/specialist_detail.html', {'specialist': specialist})