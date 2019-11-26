from django.shortcuts import redirect
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='physio-home'),

]
