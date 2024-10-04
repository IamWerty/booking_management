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

class BookingForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введіть ім\'я користувача'}))
    transport = forms.ModelChoiceField(queryset=Transport.objects.all(), empty_label="Оберіть транспорт")
    booking_end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['username', 'transport', 'booking_end_time']
