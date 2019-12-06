from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='dicom-home'),
    path('detail/(?P<value>\d+)/$', views.detail, name='dicom-detail'),
    #path('', views.dicom_to_png, name='dicom_to_png'),
    path('test/', views.dicom_to_png, name='dicom_to_png')
]
