"""ResearchPoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from recommender.views import home_view,login_view,register_view,dashboard_view,profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name = 'home'),
    path('auth/login/',login_view, name='auth_login'),
    path('auth/signup/',register_view, name='auth_signup'),
    path('dashboard/',dashboard_view, name = 'dashboard'),
    path('profile/',profile_view, name = 'profile'),
]
