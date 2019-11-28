from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='dicom-home'),
    path('about/', views.about, name='dicom-about'),
    path('dicomdraw/', views.dicom_draw, name='dicom_draw'),
]
