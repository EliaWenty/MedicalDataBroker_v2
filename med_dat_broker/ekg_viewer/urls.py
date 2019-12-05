from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='ekg-home'),
    path('detail/(?P<value>\d+)/$', views.detail, name='ekg-detail'),
    path('test/', views.ekg_to_png, name='ekg-to-png') #ekg anzeigen
]
