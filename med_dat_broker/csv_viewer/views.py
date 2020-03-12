import csv
import io
import math
import time
from random import randint

import numpy as np
import plotly.figure_factory as ff
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import re

import matplotlib.pyplot as plt

from csv_viewer.forms import CSVForm
from csv_viewer.models import csvModel, csvFileModel

vglparameter = [
    {
        'name': 'gewicht'
    },
    {
        'name': 'groesse'
    }
]


def hasdigit(inputString):
    return any(char.isalpha() for char in inputString)

def home(request):
    # csv_files = csvFileModel.objects.values('f_uuid')
    # csv_name = csvFileModel.objects.values('f_name')
    csvdict = csvFileModel.objects.all()

    # for x in csv_files:
    # csvdict[csv_name[x]]=csv_files[x]
    # print(csvdict)

    # data =csvModel.pk
    # print('printhome'+data)
    context = {
        'dataLists': csvdict,
        # 'data':data
    }
    return render(request, 'csv_viewer/csv_list.html', context)


path = "C:\\Users\\Sara\\Desktop\\arrhythmia_csv.csv"


def pathChange(self):
    path = self

    return path


# csv list Ansicht Ausgabe der Daten im CsvModel
def detail(request, value):
    pk = value
    model = get_object_or_404(csvFileModel, f_uuid=value)
    lastrow = model.f_lasttRow
    firstRow = model.f_firstRow
    listLen = []
    listFirstRow = model.c_parameter.split(',')
    for i in range(len(listFirstRow)):
        if listFirstRow[i] != ' 0':
            listLen.append(i)

    data = []
    list = []
    for i in range(firstRow, lastrow):
        csvmodel = get_object_or_404(csvModel, c_uuid=i)
        list = csvmodel.rowvalues()
        data.append(list[:len(listLen)])

    # dropdown selected ITEM
    # is_param = 'selectedparameter' in request.POST and request.POST['selectedparameter']
    # obj= Select(is_param)
    # obj.select_by_index()
    # value = request.POST['parameter']
    # selected_para = request.POST.get('parameter_list')
    # print(value)

    allColVal = []
    for column in range(len(data[0])):
        columnVal = []
        for row in range(len(data)):
            rowVal = data[row]
            columnVal.append(rowVal[column])
        allColVal.append(columnVal)
    addAll = 0

    durchschnitte = []



    for i in range(len(allColVal)):
        col = allColVal[i]
        colOut = col[2:]
        for j in range(1, len(col)):
            if hasdigit(col[j]) == False:
                addAll = addAll + round(float(col[j]), 2)


            mean = addAll / (len(col) - 1)
        durchschnitte.append({'name': col[0],
                              'avg': round(mean, 2),
                              'max': max(colOut),
                              'min': min(colOut)})

    # plt.savefig('csvauswertung.png')
    vals = []
    for colums in allColVal:
        vals.append(colums[1:len(colums)])

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        specs=[[{"type": "table"}]]
    )
    fig.add_trace(
        go.Table(header=dict(values=model.c_parameter.split(',')),
                 cells=dict(values=vals)),
        row=1, col=1
    )
    fig.update_layout(height=1000,width=1000)
    plot5 = plot(fig, output_type='div')
    context = {
        'value': data,
        'parameter': model.c_parameter.split(','),
        'auswertung': durchschnitte,
        'pk': pk,
        'tableplot':plot5
    }
    return render(request, 'csv_viewer/home.html', context)

'''
class norm1:
    def __init__(self, a1, b1, c1):
        self.a1 = a1
        self.b1 = b1
        self.c1 = c1

    def dist_curve(self):
        plt.plot(self.c1, 1 / (self.b1 * np.sqrt(2 * np.pi)) *
                 np.exp(- (self.c1 - self.a1) ** 2 / (2 * self.b1 ** 2)), linewidth=2, color='y')
        plt.show()
'''


def auswertung(request, value):
    model = get_object_or_404(csvFileModel, f_uuid=value)
    lastrow = model.f_lasttRow
    firstRow = model.f_firstRow
    listLen = []
    listFirstRow = model.c_parameter.split(',')
    for i in range(len(listFirstRow)):
        if listFirstRow[i] != ' 0':
            listLen.append(i)

    data = []
    list = []
    for i in range(firstRow, lastrow):
        csvmodel = get_object_or_404(csvModel, c_uuid=i)
        list = csvmodel.rowvalues()
        data.append(list[:len(listLen)])

    allColVal = []
    for column in range(len(data[0])):
        columnVal = []
        for row in range(len(data)):
            rowVal = data[row]
            columnVal.append(rowVal[column])
        allColVal.append(columnVal)
    addAll = 0
    durchschnitte = []

    for i in range(len(allColVal)):
        col = allColVal[i]
        colOut = col[2:]
        for j in range(1, len(col)):
            if hasdigit(col[j]) == False:
                addAll = addAll + round(float(col[j]), 2)
                mean = addAll / (len(col) - 1)
        durchschnitte.append({'name': col[0],
                              'avg': round(mean, 2),
                              'max': max(colOut),
                              'min': min(colOut)})
    np.random.seed(1)
    spaltenName=[]
    vals=[]
    for colums in allColVal:
        spaltenName.append(colums[0])
        vals.append(colums[1:len(colums)])

    #x = np.random.randn(1000)
    hist_data=[]
    for x in vals:
        x_data=[]
        for i in x:
            mu = 0
            variance = 1
            sigma = math.sqrt(variance)
            #arrangeddata = np.linspace(mu - float(i) * sigma, mu + float(i) * sigma, 100)
            if hasdigit(i) == False:
                x_data.append(float(i))
        hist_data.append(x_data)

    group_labels=[]
    for x in range(len(spaltenName)):
        group_labels.append(spaltenName[x])  #name of the dataset

    for x in hist_data[1]:
        arrangeddata = np.linspace(mu - float(x) * sigma, mu + float(x) * sigma, 100)


    #print(group_labels[1])
    #plots=[]
    #for datensatz in hist_data:
    #    for name in group_labels:
    #        a=[]
    #        a.append(datensatz)
    #        b=[]
    #        b.append(name)
    #        fig = ff.create_distplot(a, b)
    #        fig.update_layout(title_text='Normalverteilung')
    #        plot1 = plot(fig, output_type='div')
    #    plots.append(plot1)
    #fig = ff.create_distplot(hist_data, group_labels)
    #fig.update_layout(title_text='Normalverteilung')
    #plot2 = plot(fig, output_type='div')

    x_vals=[]
    y_vals=[]


    for x in range(len(hist_data)):
        x_vals.append(x)


    #fig = ff.create_dendrogram(x_vals)
    #fig.update_layout(title_text='data Auswertung')
    #plot2 = plot(fig, output_type='div')

    fig = go.Figure(data=[go.Table(header=dict(values=group_labels),
                                   cells=dict(values=vals))
                          ])
    specs = [[{"type": "table"}]]
    vorlage = [{"type": "scatter"}]
    for z in range(len(hist_data)):
        specs.append(vorlage)
    fig= make_subplots(
        rows=len(hist_data)+1, cols=1,
        shared_xaxes=True,
        specs=specs
    )
    fig.add_trace(
        go.Table(header=dict(values=group_labels),
                 cells=dict(values=vals)),
        row=1, col=1
    )
    for x in range(len(hist_data)):
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=vals[x],
                mode="lines",
                name=group_labels[x]
            ),
            row=2+x, col=1
        )
    fig.update_layout(height=4000,width=1000)
    plot5 = plot(fig, output_type='div')
    context = {
        'value': data,
        'parameter': model.c_parameter.split(','),
        'auswertung': durchschnitte,
        'plot':plot5
    }

    return render(request, 'csv_viewer/auswertung.html', context)


def selectParam(request):
    csvmodels = csvFileModel.objects.all()
    form = CSVForm()

    # csvmodel = request.POST.get('dropdown')
    print('TRIGGER')
    if request.method == "POST":
        form01 = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            preview = form01.save()
            param = preview.widget

            return render(request, 'csv_viewer/home.html', {'form': form01, 'param': param})

    context = {
        'parameter': csvmodels,
        'form': form
    }
    return render(request, 'csv_viewer/home.html', context)


# def datasource():
#    master = Tk()
#    Label(master, text="csv Path").grid(row=0)
#    e1 = Entry(master)
#    e1.grid(row=0, column=1)
#    Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)

#    mainloop()
#    path = e1.get()


def import_csv(request):
    with open(path, 'r') as file:
        data = []
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        parameter = []
        # print(header)
        dataset = []
        for i in range(len(header)):
            parameter.append(header[i])
        for row in reader:
            data.append(row)


        # for i in range(len(data)):
        #    dataset.append(data[i])
        # print(len(dataset))
        fig = make_subplots(
            rows=len(data) + 1, cols=1,
            shared_xaxes=True,
            specs=[[{"type": "table"}]]
        )
        fig.add_trace(
            go.Table(header=dict(values=parameter),
                     cells=dict(values=data)),
            row=1, col=1
        )
        plot5 = plot(fig, output_type='div')
        context = {'Vergleichsparamter': parameter,
                   'value': data}
    return render(request, 'csv_viewer/home.html', context)


@permission_required('admin.can_add_log_entry')
def contact_upload(request):
    template = "csv_viewer/contact_upload.html"

    prompt = {
        'order': 'max 14 colums'
    }

    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    # next(io_string)

    # obj = csvModel.objects.latest('c_uuid')
    obj2 = csvModel.objects.values_list('c_uuid', flat=True)
    last_row = max(obj2)
    parameterRow = last_row + 1

    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        ranInt = random_with_N_digits(9)
        milliseconds = int(round(time.time() * 1000))
        number = int(str(ranInt) + str(milliseconds))

        if len(column) < 14:
            fehlend = 14 - len(column)
            for i in range(fehlend):
                column.append(0)

        # pdb.set_trace()

        csvModel.objects.update_or_create(
            c_colOne=column[0],
            c_colTwo=column[1],
            c_colThree=column[2],
            c_colFour=column[3],
            c_colFive=column[4],
            c_colSix=column[5],
            c_colSeven=column[6],
            c_colEight=column[7],
            c_colNine=column[8],
            c_colTen=column[9],
            c_colEleven=column[10],
            c_colTwelve=column[11],
            c_colThirteen=column[12],
            c_colFourteen=column[13],
            c_number=number

        )
    # obj1 = csvModel.objects.latest('c_uuid')
    # last_last_row = obj1.c_uuid
    obj3 = csvModel.objects.values_list('c_uuid', flat=True)
    last_last_row = max(obj3)
    csvmodelParameter = get_object_or_404(csvModel, c_uuid=parameterRow)
    csvFileModel.objects.update_or_create(

        f_name=request.POST['csvname'],
        f_firstRow=last_row + 1,
        f_lasttRow=last_last_row + 1,
        c_parameter=csvmodelParameter.c_colOne + ", " +
                    csvmodelParameter.c_colTwo + ", " +
                    csvmodelParameter.c_colThree + ", " +
                    csvmodelParameter.c_colFour + ", " +
                    csvmodelParameter.c_colFive + ", " +
                    csvmodelParameter.c_colSix + ", " +
                    csvmodelParameter.c_colSeven + ", " +
                    csvmodelParameter.c_colEight + ", " +
                    csvmodelParameter.c_colNine + ", " +
                    csvmodelParameter.c_colTen + ", " +
                    csvmodelParameter.c_colEleven + ", " +
                    csvmodelParameter.c_colTwelve + ", " +
                    csvmodelParameter.c_colThirteen + ", " +
                    csvmodelParameter.c_colFourteen
    )
    context = {}
    return render(request, template, context)

