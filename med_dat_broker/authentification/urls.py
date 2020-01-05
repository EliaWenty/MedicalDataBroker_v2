from django.urls import path
from . import views
from physioNet import views as physioView


urlpatterns = [
    path('', views.home, name='authentification-home'),
    path('admin/', physioView.home, name='physioFromAuth')
]
