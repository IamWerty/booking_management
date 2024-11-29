from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import timedelta

class Transport(models.Model):
    STATUS_CHOICES = [
        ('free', 'Вільний'),
        ('busy', 'Зайнятий'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free')

    def check_and_update_status(self):
        # Якщо є активні бронювання, залишаємо статус зайнятий
        if self.booking_set.filter(booking_end_time__gt=timezone.now()).exists():
            self.status = 'busy'
        else:
            self.status = 'free'
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспортні засоби'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обов’язковий для створення користувача')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=24, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Поле для аутентифікації
    REQUIRED_FIELDS = ['username']  # Поле обов'язкове під час створення користувача

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

class Booking(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    booking_start_time = models.DateTimeField(default=timezone.now)
    booking_end_time = models.DateTimeField()

    def clean(self):
        overlapping_bookings = Booking.objects.filter(
            transport=self.transport,
            booking_start_time__lt=self.booking_end_time,
            booking_end_time__gt=self.booking_start_time
        )
        if overlapping_bookings.exists():
            raise ValidationError('Цей транспорт вже заброньовано на вибраний час.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.transport.status = 'busy'
        self.transport.save()
    
    def get_booking_duration(self):
        now = timezone.now()
        duration = self.booking_end_time - now
        return duration

    def __str__(self):
        return f"{self.username} забронював {self.transport.name} з {self.booking_start_time} по {self.booking_end_time}"

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'





@receiver(post_delete, sender=Booking)
def update_transport_status_on_booking_delete(sender, instance, **kwargs):
    instance.transport.check_and_update_status()