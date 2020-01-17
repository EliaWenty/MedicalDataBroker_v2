from django.db import models
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class csvFileModel(models.Model):
    f_uuid = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=50)
    f_firstRow = models.IntegerField(max_length=20)
    f_lasttRow = models.IntegerField(max_length=20)

    def __str__(self):
        return f'{self.pk}'

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
    c_parameter = models.CharField(max_length=200)

    # e_ppDir = models.CharField(max_length=50)
    def rowvalues(self):
        rowvalue=[]
        rowvalue.append(self.c_colOne)
        rowvalue.append(self.c_colTwo)
        rowvalue.append(self.c_colThree)
        rowvalue.append(self.c_colFour)
        rowvalue.append(self.c_colFive)
        rowvalue.append(self.c_colSix)
        rowvalue.append(self.c_colSeven)
        rowvalue.append(self.c_colEight)
        rowvalue.append(self.c_colNine)
        rowvalue.append(self.c_colTen)
        rowvalue.append(self.c_colEleven)
        rowvalue.append(self.c_colTwelve)
        rowvalue.append(self.c_colThirteen)
        rowvalue.append(self.c_colFourteen)
        return rowvalue

    def __str__(self):
        return f'{self.pk}'

    def get_parameter(self):
        return csvModel.c_parameter

