from django.urls import path
from .views import *

urlpatterns = [
    path("transport/", transport_list, name="transport"),
    path("booking/", booking_list, name="booking"),
    path("users/", users_list, name="users"),
    path("reserve/", booking_func, name="reserve"),
    path("register/", register, name="register"),
]
