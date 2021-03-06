from django.contrib import admin
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
    path('auth/admin', physioNet.views.home, name='physioFromAuth'),
    path('admin/', admin.site.urls)
    #path('admin/', include(admin.site.urls), name='authFromStart')
]
