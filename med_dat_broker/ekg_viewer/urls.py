from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='ekg-home'),
    path('detail/(?P<value>\d+)/$', views.detail, name='ekg-detail'),
    path('detail/(?P<value>\d+)/update_detail/', views.update_detail),
    path('test/<str:pk>/<str:multiplier>/', views.ekg_to_png, name='ekg-to-png') #ekg anzeigen,
]
