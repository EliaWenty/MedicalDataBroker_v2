from django.shortcuts import render
from django.http import HttpResponse
import io
import wfdb #pip install wfdb
import matplotlib.pyplot as plt
from ekg_viewer.models import ekgModel
from annoying.functions import get_object_or_None

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
    #ekgList = [f.name for f in ekgModel._meta.get_fields()]
    #print(ekgList)
    context = {
        'dataLists': ekgModel.objects.values('e_uuid')
    }
    return render(request, 'ekg_viewer/home.html', context)

def detail(request,value):
    parameter = [
        {
            'id': value
        }
        ]
    context = {
        'list' : parameter
    }
    return render(request, 'ekg_viewer/ekg_detail.html', context)

#ekg darstellen
def ekg_to_png(request, pk):

    ekgobj = get_object_or_None(ekgModel, e_uuid = pk)
    record = wfdb.rdrecord(ekgobj.e_recordName, pb_dir=ekgobj.e_ppDir)
    plt.plot(record.p_signal[1:1000])
    figure = plt.gcf() #get current figure
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0) #startposition offset standard ist 0 (kann in zukunft für sidescroll verwendet werden)
    image = buffer.read()
    return HttpResponse(image, content_type="image/png")

def about(request):
    return HttpResponse('<h1>EKG About</h1>')
