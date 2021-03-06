import pdb
import base64
import cv2
from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
import wfdb  # pip install wfdb
import matplotlib.pyplot as plt
import plotly
from plotly.offline import plot
from ekg_viewer.models import ekgModel
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from ekg_viewer.utils import render_to_pdf

EKGSINCACHE = 5
MAXSAMP = 7500
last5ekgs = {}
RTOLERANCE = 0.90
ARRYTHMIETOLERANZ = 0.4
KAMMERFLIMMERR = 0.3
TACHYTHRESH = 100
BRADYTHRESH = 60
DOPPELEINTRAGTOLERANZ = 0.3

def home(request):
    # ekgList = [f.name for f in ekgModel._meta.get_fields()]
    # print(ekgList)
    ekgdict = ekgModel.objects.all()
    context = {
        'dataLists': ekgdict
    }
    return render(request, 'ekg_viewer/home.html', context)


def detail(request, value):
    pk = value
    object = get_object_or_404(ekgModel, pk=pk)
    value = object.e_recordName
    dir = object.e_ppDir
    if value in last5ekgs:  # schauen ob record noch in der cache ist
        print("used record from cache")
        record = last5ekgs[value]
    else:
        record = wfdb.rdrecord(record_name=value, pb_dir=dir, sampto=MAXSAMP)  # record von physionet laden
    if len(last5ekgs) >= EKGSINCACHE:  # wenn mehr als 5 records in der cache sind wird sie geleert
        last5ekgs.clear()
    last5ekgs[value] = record  # record in die cache speichern
    header = wfdb.rdheader(record_name=value, pb_dir=dir)
    signal = record.p_signal
    x_values = []
    y_values = []
    y_y_values = []
    traces = []
    results = []

    for i in range(len(signal)):  # x values erstellen
        x_values.append(i)

    for i in range(len(signal)):  # y_values aus signal entpacken
        y_values.append(signal[i])
    channels = len(y_values[0])
    for c in range(channels):  # für jeden Channel des Signals einen Scatterplot erstellen
        y_y_values.clear()
        for j in range(len(y_values)):
            y_y_values.append(y_values[j][c])
        traces.append(go.Scatter(x=x_values, y=y_y_values, mode='lines', name='channel ' + str(c)))
        results.append(process_data(y_y_values, header.fs, c))
    plot_div = plot(traces, output_type='div')
    parameter = [
        {
            'recordname': value,
            'comments': header.comments,
            'samplerate': header.fs,
            'datum': header.base_date,
            'uhrzeit': header.base_time,
            'adcgain': header.adc_gain,
            'channels': channels
        }
    ]
    ekgdict = ekgModel.objects.all()
    context = {
        'list': parameter,
        'plot_div': plot_div,
        'recordname': value,
        'results': results,
        'pk': pk,
        'dataLists': ekgdict
    }
    return render(request, 'ekg_viewer/ekg_detail.html', context)


def ekg_comparison(request, value):
    ekgeintraege = ekgModel.objects.values_list('e_uuid', flat=True)
    allkeys = []
    for e in ekgeintraege:
        allkeys.append(str(e))
    value = value + ","
    value += request.POST.get('textfield', None)
    pks = value
    parameter = []
    uuids = value.split(",")
    arrchannels = {}
    tachychannels = {}
    bradychannels = {}
    flimmerchannels = {}
    puls_progression = {}
    puls_progression_flip = {}
    arrchannels_flip = {}
    tachychannels_flip = {}
    bradychannels_flip = {}
    flimmerchannels_flip = {}
    all_traces = []
    for value in uuids:
        if value not in allkeys:
            return render(request, 'ekg_viewer/errorpage.html')
        if value in last5ekgs:  # schauen ob record noch in der cache ist
            print("used record from cache")
            record = last5ekgs[value]
        else:
            ekgobject= get_object_or_404(ekgModel, pk=value)
            record = wfdb.rdrecord(record_name=ekgobject.e_recordName, pb_dir=ekgobject.e_ppDir, sampto=MAXSAMP)  # record von physionet laden
        if len(last5ekgs) >= EKGSINCACHE:  # wenn mehr als 5 records in der cache sind wird sie geleert
            last5ekgs.clear()
        last5ekgs[value] = record  # record in die cache speichern
        ekgobject = get_object_or_404(ekgModel, pk=value)
        header = wfdb.rdheader(record_name=ekgobject.e_recordName, pb_dir=ekgobject.e_ppDir)
        signal = record.p_signal
        x_values = []
        y_values = []
        y_y_values = []
        traces = []
        results = []
        for i in range(len(signal)):  # x values erstellen
            x_values.append(i)
        for i in range(len(signal)):  # y_values aus signal entpacken
            y_values.append(signal[i])
        channels = len(y_values[0])
        for c in range(channels):  # für jeden Channel des Signals einen Scatterplot erstellen
            y_y_values.clear()
            for j in range(len(y_values)):
                y_y_values.append(y_values[j][c])
            traces.append(go.Scatter(x=x_values, y=y_y_values, mode='lines', name='channel ' + str(c)))
            all_traces.append(go.Scatter(x=x_values, y=y_y_values, mode='lines', name='Record '+value+' channel ' + str(c)))
            d = process_data(y_y_values, header.fs, c)
            results.append(d)
            if c in puls_progression:
                puls_progression[c] = puls_progression[c] +" => "+str(d['puls'])+ " (in Record "+value+")"
            else:
                puls_progression[c] = "Channel "+str(c)+": "+str(d['puls'])+ " (in Record "+value+")"
            if d['tachykardie'] == 'true':
                if value in tachychannels:
                    tachychannels[value] = tachychannels[value]+", Channel "+str(c)
                else:
                    tachychannels[value] = "Record "+value+": "+"Channel "+str(c)
            if d['bradykardie'] == 'true':
                if value in bradychannels:
                    bradychannels[value] = bradychannels[value]+", Channel "+str(c)
                else:
                    bradychannels[value] = "Record "+value+": "+"Channel "+str(c)
            if d['kammerflimmern'] == 'true':
                if value in flimmerchannels:
                    flimmerchannels[value] = flimmerchannels[value]+", Channel "+str(c)
                else:
                    flimmerchannels[value] = "Record "+value+": "+"Channel "+str(c)
            if d['arrythmie'] == 'true':
                if value in arrchannels:
                    arrchannels[value] = arrchannels[value]+", Channel "+str(c)
                else:
                    arrchannels[value] = "Record "+value+": "+"Channel "+str(c)
        plot_div = plot(traces, output_type='div')

        parameter.append({
            'recordname': ekgobject.e_recordName,
            'comments': header.comments,
            'samplerate': header.fs,
            'datum': header.base_date,
            'uhrzeit': header.base_time,
            'adcgain': header.adc_gain,
            'plot_div': plot_div,
            'results': results
        })
    all_plot_div = plot(all_traces, output_type='div')
    for c in puls_progression:
        puls_progression_flip[puls_progression[c]] = c
    for c in tachychannels:
        tachychannels_flip[tachychannels[c]] = c
    for c in bradychannels:
        bradychannels_flip[bradychannels[c]] = c
    for c in arrchannels:
        arrchannels_flip[arrchannels[c]] = c
    for c in flimmerchannels:
        flimmerchannels_flip[flimmerchannels[c]] = c
    context = {
        'list': parameter,
        'puls_progression': puls_progression_flip,
        'arrchannels': arrchannels_flip,
        'tachychannels': tachychannels_flip,
        'bradychannels': bradychannels_flip,
        'flimmerchannels': flimmerchannels_flip,
        'pks': pks,
        'all_plot_div': all_plot_div
    }
    return render(request, 'ekg_viewer/ekg_comparison.html', context)


def ekg_download(request, value, format = 'json'):
    object = get_object_or_404(ekgModel, pk=value)
    value = object.e_recordName
    dir = object.e_ppDir
    record = wfdb.rdrecord(record_name=value, pb_dir=dir, sampto=MAXSAMP)
    record_dataframe = pd.DataFrame(record.p_signal, columns=record.sig_name)

    if format == 'json':
        return HttpResponse(record_dataframe.to_json(), content_type="application/json")
    elif format == 'xml':
        return HttpResponse(toXML(record_dataframe), content_type="application/xml")  # text/xml also possible if readable for casual users
    elif format == 'csv':
        return HttpResponse(record_dataframe.to_csv(), content_type="text/csv")
    elif format == 'ssv':
        return HttpResponse(record_dataframe.to_csv(sep=";"), content_type="text/csv")
    elif format == 'tsv':
        return HttpResponse(record_dataframe.to_csv(sep="\t"), content_type="text/tab-separated-values")
    elif format == 'smoothed':
        deconv = [1 / 16.0] * 16
        # First smooth data within dataframe
        for col in record_dataframe.columns:
            record_dataframe[col] = np.convolve(record_dataframe[col], deconv, 'same')
        return HttpResponse(record_dataframe.to_csv(sep="\t"), content_type="text/tab-separated-values")
    else:
        return HttpResponse("Format not supported!", content_type="text/plain")  # text/html also possible


def rowToXML(row):
    xml = ['<item>']
    for field in row.index:
        xml.append('  <field name="{0}">{1}</field>'.format(field, row[field]))
    xml.append('</item>')
    return '\n'.join(xml)


def toXML(df):
    # Full example see: https://stackoverflow.com/questions/47157536/converting-pandas-dataframe-to-xml?rq=1
    return "<?xml version=\"1.0\" ?>\n<values>\n"+'\n'.join(df.apply(rowToXML, axis=1))+"\n</values>"


def about(request):
    return HttpResponse('<h1>EKG About</h1>')


def process_data(y_values, samplerate, channel):
    first1500vals = y_values[0:1500]
    first1000vals = first1500vals[500:]
    rval = max(first1000vals)
    rvals = []
    samplesbetweenr = []
    secondsbetweenr = []
    i = 0
    for value in y_values:
        i = i+1
        if value > rval*RTOLERANCE:
            if i > samplerate*DOPPELEINTRAGTOLERANZ:
                rvals.append(value)
                samplesbetweenr.append(i)
                secondsbetweenr.append(i/samplerate)
                i = 0
                rval=value
    if rvals:
        avgsamp = avg(samplesbetweenr)
        avgsec = avg(secondsbetweenr)
        puls = 60/avgsec
        avgr = avg(rvals)
        results = {
            "channel": channel,
            "bradykardie": 'false',
            "tachykardie": 'false',
            "kammerflimmern": 'false',
            "arrythmie": 'false',
            "avgsamp": round(avgsamp, 4),
            "avgsec": round(avgsec, 4),
            "puls": round(puls, 2),
            "avgr": round(avgr, 4)
        }
        if puls > TACHYTHRESH:
            results["tachykardie"] = 'true'
        if puls < BRADYTHRESH:
            results["bradykardie"] = 'true'
        interval = secondsbetweenr[0]
        secondswofirst = secondsbetweenr
        secondswofirst.pop(0)
        for value in secondswofirst:
            if value-interval > ARRYTHMIETOLERANZ or interval-value > ARRYTHMIETOLERANZ:
                results["arrythmie"] = 'true'
                break
            interval = value
        if avgr < KAMMERFLIMMERR and results["tachykardie"] == 'true':
            results["kammerflimmern"] = 'true'
    else:
        avgsamp = 0
        avgsec = 0
        puls = 0
        puls = 0
        avgr = 0
        results = {
            "channel": channel,
            "bradykardie": 'false',
            "tachykardie": 'false',
            "kammerflimmern": 'false',
            "arrythmie": 'false',
            "avgsamp": round(avgsamp, 4),
            "avgsec": round(avgsec, 4),
            "puls": round(puls, 2),
            "avgr": round(avgr, 4)
        }
        results["tachykardie"] = 'false'
        results["bradykardie"] = 'false'
        results["arrythmie"] = 'false'
        results["kammerflimmern"] = 'false'
    return results


def avg(lst):
    try:
        return sum(lst) / len(lst)
    except:
        return 0


def generate_pdf(request, value):
    pks = value
    parameter = []
    uuids = value.split(",")
    arrchannels = {}
    tachychannels = {}
    bradychannels = {}
    flimmerchannels = {}
    puls_progression = {}
    puls_progression_flip = {}
    arrchannels_flip = {}
    tachychannels_flip = {}
    bradychannels_flip = {}
    flimmerchannels_flip = {}
    for value in uuids:
        if value in last5ekgs:  # schauen ob record noch in der cache ist
            print("used record from cache")
            record = last5ekgs[value]
        else:
            ekgobject = get_object_or_404(ekgModel, pk=value)
            record = wfdb.rdrecord(record_name=ekgobject.e_recordName, pb_dir=ekgobject.e_ppDir, sampto=MAXSAMP)  # record von physionet laden
        if len(last5ekgs) >= EKGSINCACHE:  # wenn mehr als 5 records in der cache sind wird sie geleert
            last5ekgs.clear()
        last5ekgs[value] = record  # record in die cache speichern
        ekgobject = get_object_or_404(ekgModel, pk=value)
        header = wfdb.rdheader(record_name=ekgobject.e_recordName, pb_dir=ekgobject.e_ppDir)
        signal = record.p_signal
        x_values = []
        y_values = []
        y_y_values = []
        traces = []
        results = []
        plt.plot(record.p_signal[1:1000])
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        fig.clf()
        buf.seek(0)
        image_data = buf.read()
        img = Image.open(io.BytesIO(image_data))
        # img.save("_dataarchive/0002.jpg", "JPEG")
        image = np.array(img)
        buffer = cv2.imencode('.png', image)[1].tostring()
        diffencoded = base64.b64encode(buffer).decode()
        imgStr = 'data:image/png;base64,{}'.format(diffencoded)
        for i in range(len(signal)):  # x values erstellen
            x_values.append(i)

        for i in range(len(signal)):  # y_values aus signal entpacken
            y_values.append(signal[i])
        channels = len(y_values[0])
        for c in range(channels):  # für jeden Channel des Signals einen Scatterplot erstellen
            y_y_values.clear()
            for j in range(len(y_values)):
                y_y_values.append(y_values[j][c])
            traces.append(go.Scatter(x=x_values, y=y_y_values, mode='lines', name='channel ' + str(c)))
            d = process_data(y_y_values, header.fs, c)
            results.append(d)
            if c in puls_progression:
                puls_progression[c] = puls_progression[c] + " => " + str(d['puls']) + " (in Record " + value + ")"
            else:
                puls_progression[c] = "Channel " + str(c) + ": " + str(d['puls']) + " (in Record " + value + ")"
            if d['tachykardie'] == 'true':
                if value in tachychannels:
                    tachychannels[value] = tachychannels[value] + ", Channel " + str(c)
                else:
                    tachychannels[value] = "Record " + value + ": " + "Channel " + str(c)
            if d['bradykardie'] == 'true':
                if value in bradychannels:
                    bradychannels[value] = bradychannels[value] + ", Channel " + str(c)
                else:
                    bradychannels[value] = "Record " + value + ": " + "Channel " + str(c)
            if d['kammerflimmern'] == 'true':
                if value in flimmerchannels:
                    flimmerchannels[value] = flimmerchannels[value] + ", Channel " + str(c)
                else:
                    flimmerchannels[value] = "Record " + value + ": " + "Channel " + str(c)
            if d['arrythmie'] == 'true':
                if value in arrchannels:
                    arrchannels[value] = arrchannels[value] + ", Channel " + str(c)
                else:
                    arrchannels[value] = "Record " + value + ": " + "Channel " + str(c)
        plot_div = plot(traces, output_type='div')

        parameter.append({
            'recordname': ekgobject.e_recordName,
            'comments': header.comments,
            'samplerate': header.fs,
            'datum': header.base_date,
            'uhrzeit': header.base_time,
            'adcgain': header.adc_gain,
            'image': imgStr,
            'results': results
        })
    for c in puls_progression:
        puls_progression_flip[puls_progression[c]] = c
    for c in tachychannels:
        tachychannels_flip[tachychannels[c]] = c
    for c in bradychannels:
        bradychannels_flip[bradychannels[c]] = c
    for c in arrchannels:
        arrchannels_flip[arrchannels[c]] = c
    for c in flimmerchannels:
        flimmerchannels_flip[flimmerchannels[c]] = c
    context = {
        'list': parameter,
        'puls_progression': puls_progression_flip,
        'arrchannels': arrchannels_flip,
        'tachychannels': tachychannels_flip,
        'bradychannels': bradychannels_flip,
        'flimmerchannels': flimmerchannels_flip,
        'pks': pks
    }
    pdf = render_to_pdf('ekg_viewer/ekg_comparison_for_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')