from django.urls import path
from . import views

app_name = "Lost_found_Web"
urlpatterns = [
    path("", views.index, name="index"),
    path('post/', views.post, name='post'),
    path('search/', views.search, name='search'),
    path('history/', views.history, name='history'),
]
