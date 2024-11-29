from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Transport, Booking

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.save()
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['transport', 'booking_end_time']
