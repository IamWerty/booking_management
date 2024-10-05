from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('logout/', logout_view, name='logout'),
    path("transport/", transport_list, name="transport"),
    path("booking/", booking_list, name="booking"),
    path("users/", users_list, name="users"),
    path("reserve/", booking_func, name="reserve"),
    path("register/", register, name="register"),
    path('login/', login_view, name='login'),
    path('account_info/', account_info, name='account_info'),
    path('contact/', contact, name="contact"),
]
