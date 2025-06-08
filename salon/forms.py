# salon/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Booking, Rating, Service

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class BookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Услуга",
        widget=forms.Select(
            attrs={
                'class': 'border border-gray-300 p-2 w-full rounded',
            }
        )
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',                       # HTML5
                'class': 'border border-gray-300 p-2 w-full rounded',
            }
        ),
        label='Дата',
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',                       # HTML5
                'class': 'border border-gray-300 p-2 w-full rounded',
            }
        ),
        label='Время',
    )

    class Meta:
        model = Booking
        fields = ["service", "date", "time"]

class BookingEditForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'border border-gray-300 p-2 w-full rounded',
        }),
        label='Дата'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'border border-gray-300 p-2 w-full rounded',
        }),
        label='Время'
    )

    class Meta:
        model = Booking
        # Без поля "service"
        fields = ['date', 'time']


class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(
        label='Оценка',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2',
            'placeholder': 'Оценка от 1 до 5'
        })
    )
    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2',
            'rows': 4,
            'placeholder': 'Оставьте ваш отзыв...'
        }),
        required=False
    )
    class Meta:
        model = Rating
        fields = ["rating", "comment"]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "specialist", "photo", "duration_minutes", "details"]
    widgets = {
        'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 w-full rounded'}),
        'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 w-full rounded', 'rows': 3}),
        'price': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 w-full rounded'}),
        'specialist': forms.Select(attrs={'class': 'border border-gray-300 p-2 w-full rounded'}),
        'photo': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 p-2 w-full rounded'}),
        'duration_minutes': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 w-full rounded'}),
        'details': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 w-full rounded', 'rows': 3}),
    }
