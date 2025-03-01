# salon/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Specialist, Salon, Booking, Rating
from .forms import RegistrationForm, BookingForm, RatingForm

def index(request):
    return render(request, 'salon/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверные логин или пароль.")
    return render(request, 'salon/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'salon/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'salon/profile.html')

@login_required
def booking_list(request):
    """
    Список всех бронирований пользователя (или всех, если это админ).
    """
    if request.user.is_staff:
        # Если это владелец салона (или админ Django), показать все
        bookings = Booking.objects.select_related('specialist', 'user').all()
    else:
        # Обычный пользователь
        bookings = request.user.bookings.select_related('specialist')
    return render(request, 'salon/booking_list.html', {'bookings': bookings})

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'salon/booking_create.html', {'form': form})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Проверяем, что либо пользователь владелец бронирования, либо staff
    if booking.user != request.user and not request.user.is_staff:
        messages.error(request, "У вас нет доступа к этой записи.")
        return redirect('booking_list')
    return render(request, 'salon/booking_detail.html', {'booking': booking})

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user == request.user or request.user.is_staff:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, "Запись успешно отменена.")
    else:
        messages.error(request, "У вас нет прав отменять эту запись.")
    return redirect('booking_list')

def specialist_list(request):
    specialists = Specialist.objects.all()
    return render(request, 'salon/specialist_list.html', {'specialists': specialists})

def specialist_detail(request, pk):
    specialist = get_object_or_404(Specialist, pk=pk)
    return render(request, 'salon/specialist_detail.html', {'specialist': specialist})

@login_required
def add_rating(request, booking_id):
    """
    Добавляем оценку/отзыв. Предполагаем, что запись уже завершена (status = 'finished').
    """
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        messages.error(request, "Вы не можете оставить отзыв для чужой записи.")
        return redirect('booking_list')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_obj = form.save(commit=False)
            rating_obj.booking = booking
            rating_obj.save()
            messages.success(request, "Спасибо за отзыв!")
            return redirect('booking_list')
    else:
        form = RatingForm()
    return render(request, 'salon/add_rating.html', {'form': form, 'booking': booking})


@login_required
def admin_panel(request):
    """
    Пример самой простой "админ‑панели" для владельца салона:
    список всех бронирований, быстрое подтверждение и т.д.
    """
    if not request.user.is_staff:
        messages.error(request, "У вас нет доступа к админ‑панели.")
        return redirect('home')
    bookings = Booking.objects.select_related('specialist', 'user').all()
    return render(request, 'salon/admin_panel.html', {'bookings': bookings})


@login_required
def stats_view(request):
    """
    Статистика: например, количество записей, средняя оценка и проч.
    """
    if not request.user.is_staff:
        messages.error(request, "Только для персонала.")
        return redirect('home')

    total_bookings = Booking.objects.count()
    finished_bookings = Booking.objects.filter(status='finished').count()
    ratings = Rating.objects.all()
    if ratings.exists():
        avg_rating = sum(r.rating for r in ratings) / ratings.count()
    else:
        avg_rating = 0
    
    context = {
        'total_bookings': total_bookings,
        'finished_bookings': finished_bookings,
        'avg_rating': avg_rating
    }
    return render(request, 'salon/stats.html', context)
