from django.urls import path
from . import views

study = [
    {
        'serie': '1',
        'patient': 'Elia Wenty',
        
    }
]

urlpatterns = [
    path('', views.home, name='dicom-home'),
    path('about/', views.about, name='dicom-about'),

]
