from django.urls import path, re_path
from . import views



urlpatterns = [
    path('', views.home, name='ekg-home'),
    re_path('detail/(?P<value>\d+)/$', views.detail, name='ekg-detail'),
    re_path('detail/(?P<value>\d+)/update_detail/', views.update_detail),
    re_path('test/<str:pk>/<str:multiplier>/', views.ekg_to_png, name='ekg-to-png') #ekg anzeigen,
]
