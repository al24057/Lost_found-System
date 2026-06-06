from django.urls import path
from . import views

app_name = "Lost_found_Web"
urlpatterns = [
    path('', views.index, name="home"),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('post/', views.post, name='post'),
    path('post/edit/<int:pk>/', views.post, name='post_edit'),
    path('search/', views.search, name='search'),
    path('history/', views.history, name='history'),
]
