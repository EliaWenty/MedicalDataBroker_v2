from django.shortcuts import render
from django.http import HttpResponse

import csv
from tkinter import *

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
        #print(header)
        dataset = []
        for i in range(len(header)):
            parameter.append(header[i])

        for row in reader:
            data.append(row)
        context = {'Vergleichsparamter': parameter,
                   'value': data}

        #for i in range(len(data)):
        #    dataset.append(data[i])
        #print(len(dataset))
    return render(request, 'csv_viewer/home.html', context)
