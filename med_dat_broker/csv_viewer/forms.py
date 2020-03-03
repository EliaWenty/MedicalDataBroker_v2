from django import forms
from django.forms import ModelForm

from csv_viewer.models import csvModel, csvFileModel

class CSVForm(ModelForm):
    csvmodels = csvFileModel.objects.values('c_parameter')
    #f_uuid = forms.AutoField(primary_key=True)
    #f_name = forms.CharField()
    #f_firstRow = forms.IntegerField()
    #f_lasttRow = forms.IntegerField()
    widget= forms.Select(choices=csvmodels)

class Meta:
    model=CSVForm
    fields=['Dropdown']
    widgets ={
        'Dropdown': forms.Select(attrs={'param':'age'})
    }