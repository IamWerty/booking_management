from django.shortcuts import redirect, render
from .models import Transport, Booking, CustomUser
# Create your views here.
def transport_list(request):
    transport_list = Transport.objects.all()
    return render(request, "booking_app/transport_list.html", {'transport_list':transport_list})

def booking_list(request):
    booking_list = Booking.objects.all()
    return render(request, "booking_app/booking_list.html", {"booking_list":booking_list})

def Users_list(request):
    users_list = CustomUser.objects.all()
    return render(request, "booking_app/users_list.html", {"users_list":users_list})

def booking_func(request):
    transport_list = Transport.objects.filter(status='free')

    if request.method == "POST":
        transport_id = request.POST.get("transport")
        user_username = request.POST.get("username")
        hours = int(request.POST.get("booking_time"))

        try:
            user = CustomUser.objects.get(username=user_username)
        except CustomUser.DoesNotExist:
            return render(request, 'booking_app/error.html', {'error': 'Користувача не знайдено'})

        Booking.objects.create(
            transport=Transport.objects.get(id=transport_id),
            username=user_username,
            total_price = Booking.create_booking(username=user_username, transport=transport_id, hours=hours)
        )

        return redirect("success")

    return render(request, "booking_app/reserve.html", {'transport_list': transport_list})


# def user_add_func(request):
#     if request.method == "POST":
#         user_username = request.POST.get("user")
#         try:
#             user = CustomUser.objects.get(username=user_username)
#         except CustomUser.DoesNotExist:
#             return render(request, 'bookingapp/error.html', {'error': 'Користувача не знайдено'})
        
#         CustomUser.objects.create(
#             user = CustomUser.objects.get(username=user_username),
#             username = CustomUser.objects.get(username=user_name)
#         )
#         return redirect("register")
#     return render(request, "booking_app/user_register.html")