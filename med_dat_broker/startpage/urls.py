from django.shortcuts import redirect
from django.urls import path, include
from . import views
# from dicom_viewer import views as dicomViews

import dicom_viewer

app_dcm = 'dicom_viewer'

urlpatterns = [
    path('', views.home, name='startpage-home'),
    path('dicom/', dicom_viewer.views.home, name='dicomFromStart')
]
