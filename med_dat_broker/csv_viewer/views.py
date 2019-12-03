from django.shortcuts import render
from django.http import HttpResponse


vglparameter = [
    {
        'name':'gewicht'
    },
    {
        'name':'groesse'
    }
]
def home(request):
    context = {
        'Vergleichsparamter': vglparameter
    }
    return render(request, 'csv_viewer/home.html',context)

