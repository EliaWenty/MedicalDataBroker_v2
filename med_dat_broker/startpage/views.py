from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import dicom_viewer
import ekg_viewer


def home(request):
    return render(request, 'startpage/home.html')


def dicom(request):
    return HttpResponseRedirect(dicom_viewer.urls)

def ekg(request):
    return render(request,'ekg_viewer/home.html')
