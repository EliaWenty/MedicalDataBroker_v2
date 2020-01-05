import pdb

from django.shortcuts import render
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


def home(request):
    # ekgList = [f.name for f in ekgModel._meta.get_fields()]
    # print(ekgList)
    context = {
        'dataLists': ekgModel.objects.values('e_recordName')
    }
    return render(request, 'ekg_viewer/home.html', context)


def detail(request, value):
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

def ekg_comparison(request, value):
    value =value+","
    value += request.POST.get('textfield', None)
    parameter =[]
    plot_divs =[]
    record_names=value.split(",")
    for value in record_names:
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

        parameter.append({
            'recordname': value,
            'comments': header.comments,
            'samplerate': header.fs,
            'datum': header.base_date,
            'uhrzeit': header.base_time,
            'adcgain': header.adc_gain,
            'plot_div': plot_div
        })
        plot_divs.append(plot_div)

    #context for template
    context = {
        'list': parameter
    }
    return render(request, 'ekg_viewer/ekg_comparison.html', context)

def about(request):
    return HttpResponse('<h1>EKG About</h1>')
