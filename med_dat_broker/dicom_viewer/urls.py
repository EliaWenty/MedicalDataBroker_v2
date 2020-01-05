from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='dicom-home'),
    path('detail/<str:value>/', views.detail, name='dicom-detail'),
    path('draw_dicom/', views.dicom_to_png, name='dicom-to-png')
]
