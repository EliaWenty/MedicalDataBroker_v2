from django.shortcuts import redirect
from django.urls import path, include
from . import views
# from dicom_viewer import views as dicomViews

import dicom_viewer
import ekg_viewer
import csv_viewer
import authentification
import physioNet
#app_dcm = 'dicom_viewer'

urlpatterns = [
    path('', views.home, name='startpage-home'),
    path('dicom/', dicom_viewer.views.home, name='dicomFromStart'),
    path('ekg/', ekg_viewer.views.home, name='ekgFromStart'),
    path('csv/', csv_viewer.views.home, name='csvFromStart'),
    path('auth/physio', physioNet.views.home, name='physioFromAuth'),
    path('auth/',authentification.views.home, name='authFromStart')
]
