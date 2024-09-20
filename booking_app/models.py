from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Модель Transport (Транспорт)
class Transport(models.Model):
    STATUS_CHOICES = [
        ('free', 'Вільний'),
        ('busy', 'Зайнятий'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспортні засоби'

class CustomUser(models.Model):  # Розширена модель для користувачів, якщо потрібна додаткова інформація
    username = models.CharField(max_length=24, default="Jonh Doe")
    password = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Booking(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    booking_time_start = models.DateTimeField(auto_now_add=True)
    # days = models.DateField()
    # booking_time_end = booking_time_start + days

    def clean(self):
        overlapping_bookings = Booking.objects.filter(
            transport=self.transport,
            booking_time_start__lt=self.booking_time_end,
            booking_time_end__gt=self.booking_time_start
        )
        if overlapping_bookings.exists():
            raise ValidationError('Цей транспорт вже заброньовано на вибраний час.')

    def calculate_total_price(self, days):
        return days * self.transport.price

    def save(self, *args, **kwargs):
        self.clean()
        if self.booking_time_start <= self.booking_time_end:
            self.transport.status = 'busy'
        else:
            self.transport.status = 'free'
        self.transport.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} забронював {self.transport.name} з {self.booking_time_start} по {self.booking_time_end}"

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
