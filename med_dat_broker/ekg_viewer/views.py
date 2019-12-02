from django.shortcuts import render
from django.http import HttpResponse
import io
import wfdb #pip install wfdb

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
path = "_dataarchive/ARR_01"
def home(request):
    context = {
        'dataLists': dataList
    }
    return render(request, 'ekg_viewer/home.html', context)

#ekg darstellen
def ekg_to_png(request):
    record = wfdb.rdrecord(path)
    ekgplot.plot(record.p_signal[1:1000])
    figure = ekgplot.gcf() #get current figure
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)
    image = buffer.read()
    return HttpResponse(image, content_type="image/png")

def about(request):
    return HttpResponse('<h1>EKG About</h1>')
