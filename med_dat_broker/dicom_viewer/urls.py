from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='dicom-home'),
    #path('about/', views.about, name='dicom-about'),
    #path('', views.dicom_to_png, name='dicom_to_png'),
    path('test/', views.dicom_to_png, name='dicom_to_png')
]
