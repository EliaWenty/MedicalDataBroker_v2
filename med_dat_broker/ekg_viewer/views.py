import pdb

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
import wfdb  # pip install wfdb
import matplotlib.pyplot as plt
import plotly
from plotly.offline import plot
from ekg_viewer.models import ekgModel
import plotly.graph_objs as go

EKGSINCACHE = 5
MAXSAMP = 7500
last5ekgs = {}

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
    # ekgList = [f.name for f in ekgModel._meta.get_fields()]
    # print(ekgList)
    context = {
        'dataLists': ekgModel.objects.values('e_uuid')
    }
    return render(request, 'ekg_viewer/home.html', context)


def detail(request, value):
    object = get_object_or_404(ekgModel, pk = value)
    value = object.e_recordName
    if value in last5ekgs:  # schauen ob record noch in der cache ist
        print("used record from cache")
        record = last5ekgs[value]
    else:
        record = wfdb.rdrecord(record_name=value, pb_dir='mitdb', sampto=MAXSAMP)  # record von physionet laden
    if len(last5ekgs) >= EKGSINCACHE:  # wenn mehr als 5 records in der cache sind wird sie geleert
        last5ekgs.clear()
    last5ekgs[value] = record  # record in die cache speichern

    signal = record.p_signal
    x_values = []
    y_values = []
    y_y_values = []
    traces = []

    for i in range(len(signal)):  # x values erstellen
        x_values.append(i)

    for i in range(len(signal)):  # y_values aus signal entpacken
        y_values.append(signal[i])
    channels = len(y_values[0])
    for c in range(channels):  # für jeden Channel des Signals einen Scatterplot erstellen
        for j in range(len(y_values)):
            y_y_values.append(y_values[j][c])
        traces.append(go.Scatter(x=x_values, y=y_y_values, mode='lines', name='channel ' + str(c)))

    plot_div = plot(traces, output_type='div')
    header = wfdb.rdheader(record_name=value, pb_dir='mitdb')

    parameter = [
        {
            'recordname': value,
            'comments': header.comments,
            'samplerate': header.fs,
            'datum': header.base_date,
            'uhrzeit': header.base_time,
            'adcgain': header.adc_gain
        }
    ]
    context = {
        'list': parameter,
        'plot_div': plot_div
    }
    return render(request, 'ekg_viewer/ekg_detail.html', context)


def update_detail(request, value):
    multiplier = request.POST.get('textfield')
    parameter = [
        {
            'recordname': value,
            'multiplier': multiplier
        }
    ]
    context = {
        'list': parameter
    }
    return render(request, 'ekg_viewer/ekg_detail.html', context)

"""
# ekg darstellen
def ekg_to_png(request, pk, multiplier):
    record = wfdb.rdrecord('_dataarchive/ARR_01', channels=[0])
    signal = record.p_signal
    # pdb.set_trace()
    # if len(last5ekgs) >= EKGSINCACHE:
    # last5ekgs.clear()
    #  last5ekgs[pk] = record
    plt.plot(signal)
    figure = plt.gcf()  # get current figure
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)  # startposition offset standard ist 0 (kann in zukunft für sidescroll verwendet werden)
    image = buffer.read()
    # signal = record.p_signal
    # fs = record.fs
    # plot_div = plot([go.Scatter(x=signal[0], y=signal[1:], mode='lines', name='test')], output_type='div')
    return HttpResponse(image, content_type="image/png")
"""

def about(request):
    return HttpResponse('<h1>EKG About</h1>')
