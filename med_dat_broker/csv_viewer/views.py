from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

import csv
from tkinter import *

from csv_viewer.models import csvModel

vglparameter = [
    {
        'name': 'gewicht'
    },
    {
        'name': 'groesse'
    }
]


def home(request):
    context = {
        'Vergleichsparamter': vglparameter
    }
    print(context)
    return render(request, 'csv_viewer/home.html', context)


path = "C:\\Users\\Sara\\Desktop\\arrhythmia_csv.csv"


def pathChange(self):
    path = self
    return path


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
    template = "contact_upload.html"

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
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = csvModel.objects.update_or_create(
            colOne=column[0],
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
            c_colFourteen=column[13]
        )
    context = {}
    return render(request, template, context)
