from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='ekg-home'),
    path('detail/<str:value>/', views.detail, name='ekg-detail'),
    path('detail/<str:value>/comparison/', views.ekg_comparison, name='ekg-comparison')
]
