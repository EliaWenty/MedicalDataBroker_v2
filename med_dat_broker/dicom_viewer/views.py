from django.shortcuts import render
from django.http import HttpResponse

study = [
    {
        'serie': '1',
        'patient': 'Elia Wenty',
        'picture': 'DICOM_2.JPEG'

    },
    {
        'serie': '2',
        'patient': 'Elia Wenty',
        'picture': 'DICOM_3.JPEG'

    }
]

def home(request):
    context = {
        'study': study
    }
    return render(request, 'dicom_viewer/home.html', context)

def about(request):
    return HttpResponse('<h1>DCM About</h1>')
