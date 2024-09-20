from django.urls import path
from .views import *

urlpatterns = [
    path("transport/", transport_list, name="transport"),
    path("booking/", booking_list, name="booking"),
    path("users/", Users_list, name="users"),
    path("reserve/", booking_func, name="reserve"),
    # path("register/", user_add_func, name="register"),
    path("error/", booking_func, name="error"),
    path("success/", booking_func, name="success"),
]
