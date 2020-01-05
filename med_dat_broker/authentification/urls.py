from django.urls import path
from . import views
from physioNet import views as physioView

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]