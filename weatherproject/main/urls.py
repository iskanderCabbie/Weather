from django.urls import path
from . import views

urlpatterns = [
    path("", views.weather_view, name="weather"),
    path("api/history/", views.history_api, name="history_api"),
    path("api/history/user/", views.user_history_api, name="user_history_api"),
]

