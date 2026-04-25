"""
URL configuration for Lost_found_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

def disable_view(request):
    return HttpResponseForbidden("この機能は使えません")

def custom_login(request):
    return render(request, "account/login.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_login),
    path('accounts/', include('allauth.urls')),
    
    path('accounts/login/', disable_view),
    path('accounts/signup/', disable_view),
    
    path('', include("Lost_found_Web.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
