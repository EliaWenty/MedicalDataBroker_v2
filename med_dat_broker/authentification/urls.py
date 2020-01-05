from django.urls import path
from . import views
from physioNet import views as physioView


#urlpatterns = [
    #path('', views.home, name='authentification-home'),
    #path('auth/', physioView.home, name='physioFromAuth')
#]
# urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]