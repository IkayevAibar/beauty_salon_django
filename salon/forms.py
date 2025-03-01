# salon/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Rating

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["specialist", "salon", "date", "time"]

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "comment"]
