from django.contrib import admin
from .models import Transport, Booking, CustomUser
# Register your models here.
admin.site.register(Transport)
admin.site.register(Booking)
admin.site.register(CustomUser)