from django.shortcuts import redirect, render
from .models import Transport, Booking, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, BookingForm
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta


from decimal import Decimal

def check_bookings():
    now = timezone.now()
    
    # Отримуємо всі бронювання, де час закінчився
    expired_bookings = Booking.objects.filter(booking_end_time__lte=now)
    
    for booking in expired_bookings:
        # Обчислюємо загальний рахунок
        total_time = (booking.booking_end_time - booking.booking_start_time).total_seconds() / 3600  # Різниця в годинах
        transport_price = booking.transport.price  # Ціна транспорту в Decimal
        
        # Конвертуємо total_time до Decimal перед множенням
        total_cost = Decimal(total_time) * transport_price
        
        # Видаляємо бронювання після повідомлення користувача
        message = f"Бронювання на {booking.transport.name} закінчилось, ваш підсумковий рахунок: {total_cost}"
        
        # Логіка для повідомлення користувача та видалення бронювання
        booking.delete()

    return True


# Список транспорту
def transport_list(request):
    check_bookings()
    transport_list = Transport.objects.filter(status='free')
    return render(request, "booking_app/transport_list.html", {'transport_list':transport_list})

# Список бронювань
def booking_list(request):
    check_bookings()
    booking_list = Booking.objects.all()
    return render(request, "booking_app/booking_list.html", {"booking_list":booking_list})

# Список користувачів
def users_list(request):
    users_list = CustomUser.objects.all()
    return render(request, "booking_app/users_list.html", {"users_list":users_list})

@login_required
def booking_func(request):
    transport_list = Transport.objects.filter(status='free')

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            user_username = request.user
            transport = form.cleaned_data['transport']
            booking_end_time = form.cleaned_data['booking_end_time']
            booking_end_time -= timedelta(hours=3)
            

            Booking.objects.create(
                username=user_username,
                transport=transport,
                booking_end_time=booking_end_time
            )

            return redirect("transport")

    else:
        form = BookingForm()

    return render(request, "booking_app/reserve.html", {'form': form, 'transport_list': transport_list})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('reserve')  # Переадресація на сторінку бронювання
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reserve')  # Переадресація на сторінку бронювання або іншу потрібну сторінку
        else:
            return render(request, 'booking_app/login.html', {'error': 'Невірний логін або пароль'})
    else:
        return render(request, 'booking_app/login.html')
    
def index(request):
    return render(request, "booking_app/index.html")

@login_required
def account_info(request):
    return render(request, 'booking_app/account_info.html')

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

def contact(request):
    return render(request, "booking_app/contact.html")