from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'csv_viewer/home.html')

