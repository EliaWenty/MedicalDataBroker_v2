from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='ekg-home'),
    path('detail/<str:value>/', views.detail, name='ekg-detail'),
    path('detail/<str:value>/comparison/', views.ekg_comparison, name='ekg-comparison'),
    path('ekg_download/<str:format>/<str:value>/', views.ekg_download, name='ekg_download')
]
