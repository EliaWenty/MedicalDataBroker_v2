from django.shortcuts import render
from django.http import HttpResponse

dataList = [
    {
        'serie': '1',
        'patient': 'Elia Wenty',
        'picture': 'EKG_2.JPEG'

    },
    {
        'serie': '2',
        'patient': 'Elia Wenty',
        'picture': 'EKG_3.JPEG'

    }
]

def home(request):
    context = {
        'dataLists': dataList
    }
    return render(request, 'ekg_viewer/home.html', context)

def about(request):
    return HttpResponse('<h1>EKG About</h1>')
