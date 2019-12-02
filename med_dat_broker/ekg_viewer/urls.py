from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='ekg-home'),
    path('test/', views.ekg_to_png, name='ekg-to-png'),
]
