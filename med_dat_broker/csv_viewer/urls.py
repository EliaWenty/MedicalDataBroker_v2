from django.urls import path

from csv_viewer.views import contact_upload
from . import views



urlpatterns = [
    path('', views.home, name='csv-home'),
    path('/test', views.import_csv, name='import_csv'),
    path('/test',views.import_csv,name='pathChange'),
    path('/upload-csv/', contact_upload, name='contact_upload')
]
