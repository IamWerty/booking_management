from django.urls import path
from .views import transport_list


urlpatterns = [
    path("", transport_list, name="booking")
]