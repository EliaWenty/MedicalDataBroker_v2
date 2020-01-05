from django.contrib import admin

from csv_viewer.models import csvModel, csvFileModel

admin.site.register(csvModel)
admin.site.register(csvFileModel)