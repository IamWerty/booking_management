from django.shortcuts import redirect, render
from .models import Transport, Booking, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, BookingForm

# Список транспорту
def transport_list(request):
    transport_list = Transport.objects.filter(status='free')
    return render(request, "booking_app/transport_list.html", {'transport_list':transport_list})

# Список бронювань
def booking_list(request):
    booking_list = Booking.objects.all()
    return render(request, "booking_app/booking_list.html", {"booking_list":booking_list})

# Список користувачів
def users_list(request):
    users_list = CustomUser.objects.all()
    return render(request, "booking_app/users_list.html", {"users_list":users_list})

def booking_func(request):
    transport_list = Transport.objects.filter(status='free')

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            transport = form.cleaned_data['transport']
            booking_end_time = form.cleaned_data['booking_end_time']

            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return render(request, 'booking_app/error.html', {'error': 'Користувача не знайдено'})

            Booking.objects.create(
                username=user,
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