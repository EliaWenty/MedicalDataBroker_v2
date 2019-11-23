from django.shortcuts import redirect
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.login, name='startpage-home'),
    path('physioNet', views.)
]
