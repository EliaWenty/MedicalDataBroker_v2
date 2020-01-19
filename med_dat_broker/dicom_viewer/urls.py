from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='dicom-home'),
    path('detail/<str:value>/', views.detail, name='dicom-detail'),
    #path('draw_dicom/', views.dicom_to_png, name='dicom_to_png'),
    path('detail/<str:value>/comparison/', views.dicom_comparison, name='dicom-comparison'),
    #path('vergleich/<str:value>/', views.dicom_compare, name='dicom-compare'),
    path('dicom_download/<str:format>/<str:value>/', views.dicom_download, name='dicom_download'),
    path('dicom_pdf_download/<str:value>/', views.dicom_pdf, name='dicom_pdf_download')
]
