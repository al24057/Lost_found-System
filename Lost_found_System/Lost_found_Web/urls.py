from django.urls import path
from . import views

app_name = "Lost_found_Web"
urlpatterns = [
    path("", views.index, name="index"),
]
