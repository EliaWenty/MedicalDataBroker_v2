from django.urls import path


from . import views



urlpatterns = [
    path('', views.home, name='csv-home'),
    path('/test', views.import_csv, name='import_csv'),
    path('/test',views.import_csv,name='pathChange'),
    path('/upload-csv/', views.contact_upload, name='contact_upload'),
    path('detail/<str:value>/', views.detail, name='csv-detail')
]
