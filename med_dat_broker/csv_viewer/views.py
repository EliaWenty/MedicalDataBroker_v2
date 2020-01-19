import pdb

from django.shortcuts import render, get_object_or_404
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from random import randint
import time

import csv
from tkinter import *

from csv_viewer.models import csvModel, csvFileModel

vglparameter = [
    {
        'name': 'gewicht'
    },
    {
        'name': 'groesse'
    }
]


def home(request):
    csv_files = csvFileModel.objects.values('f_uuid')
    csv_name = csvFileModel.objects.values('f_name')
    # data =csvModel.pk
    # print('printhome'+data)
    context = {
        'dataLists': csv_files,
        'names': csv_name,
        # 'data':data
    }
    return render(request, 'csv_viewer/csv_list.html', context)


path = "C:\\Users\\Sara\\Desktop\\arrhythmia_csv.csv"


def pathChange(self):
    path = self

    return path


# csv list Ansicht Ausgabe der Daten im CsvModel
def detail(request, value):
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


    context = {
        'value': data,
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
        context = {'Vergleichsparamter': parameter,
                   'value': data}

        # for i in range(len(data)):
        #    dataset.append(data[i])
        # print(len(dataset))
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
        print(column)
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
