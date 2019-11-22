from django.urls import path
from . import views
#from ..dicom_viewer import views as dicomViews
from dicom_viewer.views import home

urlpatterns = [
    path('', views.home, name='startpage-home'),
    path('dicom/', sys, name='dicomFromStart')
]
