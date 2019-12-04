from django.db import models
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class ekgModel(models.Model):
    e_uuid = models.AutoField(primary_key=True)
    e_recordName = models.CharField(max_length=50)
    e_ppDir = models.CharField(max_length=50)
