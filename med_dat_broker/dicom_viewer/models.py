from django.db import models
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class dcmModel(models.Model):
    d_uuid = models.AutoField(primary_key=True)
    d_patientuid = models.CharField(max_length=300)
    d_seriesuid = models.CharField(max_length=300)
    d_studyuid = models.CharField(max_length=300)
    d_imageuid = models.CharField(max_length=300)
    d_sopinstanceuid = models.CharField(max_length=300)