from django.db import models
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class csvModel(models.Model):
    c_uuid = models.AutoField(primary_key=True)
    c_colOne = models.CharField(max_length=50)
    c_colTwo = models.CharField(max_length=50)
    c_colThree = models.CharField(max_length=50)
    c_colFour = models.CharField(max_length=50)
    c_colFive = models.CharField(max_length=50)
    c_colSix = models.CharField(max_length=50)
    c_colSeven = models.CharField(max_length=50)
    c_colEight = models.CharField(max_length=50)
    c_colNine = models.CharField(max_length=50)
    c_colTen = models.CharField(max_length=50)
    c_colEleven = models.CharField(max_length=50)
    c_colTwelve = models.CharField(max_length=50)
    c_colThirteen = models.CharField(max_length=50)
    c_colFourteen = models.CharField(max_length=50)

    # e_ppDir = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pk}'
