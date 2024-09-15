from django.shortcuts import render
from .models import Transport
# Create your views here.
def transport_list(request):
    transport_list = Transport.objects.all()
    return render(request, "booking_app/transport_list.html", {'transport_list':transport_list})