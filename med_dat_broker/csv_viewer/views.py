from django.shortcuts import render, get_object_or_404
import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

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
    csv_name= csvFileModel.objects.values('f_name')
    #data =csvModel.pk
    #print('printhome'+data)
    context = {
        'dataLists': csv_files,
        'names':csv_name,
        #'data':data
    }
    return render(request, 'csv_viewer/csv_list.html', context)
path = "C:\\Users\\Sara\\Desktop\\arrhythmia_csv.csv"

def pathChange(self):
    path = self

    return path

#csv list Ansicht Ausgabe der Daten im CsvModel
def detail(request, value):
    model=get_object_or_404(csvFileModel,f_uuid=value)
    lastrow = model.f_lasttRow
    firstRow= model.f_firstRow
    #lastrow=csvFileModel.objects.values_list('f_lasttRow',flat=True)
    #firstRow = csvFileModel.objects.values_list('f_firstRow' ,flat=True)
    #object = get_object_or_404(csvFileModel,pk=value)
    #value = object.f_name
    #datalist = get_object_or_404(csvModel,pk= object)
    #uuids=[]
    #data=[]
    colOneval=[]
    colTwoval = []
    colThreeval = []
    colFourval = []
    colFiveval = []
    colSixval = []
    colSevenval = []
    colEightval = []
    colNineval = []
    colTenval = []
    colElevenval = []
    colTwelveval = []
    colThirteenval = []
    colFourteenval=[]

    #obj= csvModel.objects.values_list('c_uuid',flat=True)
    print('last')
    print(lastrow)
    print('first')
    print(firstRow)
    files= csvFileModel.objects.values_list('f_uuid',flat=True)
    filemodels=len(files)
    print(filemodels)
    #for x in range(filemodels):
    data=[]
    datavalues = []
    for i in range(firstRow,lastrow):
        csvmodel =get_object_or_404(csvModel,c_uuid=i)
        colOneval.append(csvmodel.c_colOne)
        colTwoval.append(csvmodel.c_colTwo)
        colThreeval.append(csvmodel.c_colThree)
        colFourval.append(csvmodel.c_colFour)
        colFiveval.append(csvmodel.c_colFive)
        colSixval.append(csvmodel.c_colSix)
        colSevenval.append(csvmodel.c_colSeven)
        colEightval.append(csvmodel.c_colEight)
        colNineval.append(csvmodel.c_colNine)
        colTenval.append(csvmodel.c_colTen)
        colElevenval.append(csvmodel.c_colEleven)
        colTwelveval.append(csvmodel.c_colTwelve)
        colThirteenval.append(csvmodel.c_colThirteen)
        colFourteenval.append(csvmodel.c_colFourteen)
        data.append(csvmodel.rowvalues())
    for c in range(len(data)):
        for p in range(len(data[c])):
            datavalues.append(data[p])
    #Tabellenausgabe der Datensätze
    #data = [d.strip() for d in data]
    #data= [f"<tr><td>{d}</tr>" for d in data if d.strip() != ""]
    vglparameter= csvmodel.c_parameter
    #data = "<table border=1>" + "".join(data) + "</table>"
        #data.append(colOneval)
        #data.append(colTwoval)
        #data.append(colThreeval)
        #data.append(colFourval)
        #data.append(colFiveval)
        #data.append(colSixval)
        #data.append(colSevenval)
        #data.append(colEightval)
        #data.append(colNineval)
        #data.append(colTenval)
        #data.append(colElevenval)
        #data.append(colTwelveval)
        #data.append(colThirteenval)
        #data.append(colFourteenval)
            #for ids in values:
                #data=get_object_or_404(csvModel,pk=ids)
                #datalist.append(data)
                #ids=ids+1
    context = {
        'value': data,
        'parameter': vglparameter
        #'csvname': ,
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
    next(io_string)


    obj = csvModel.objects.latest('c_uuid')
    last_row = obj.c_uuid
    row = 1
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        row = row + 1
        csvModel.objects.update_or_create(
            c_parameter= column[0],
            c_colOne=column[1],
            c_colTwo=column[2],
            c_colThree=column[3],
            c_colFour=column[4],
            c_colFive=column[5],
            c_colSix=column[6],
            c_colSeven=column[7],
            c_colEight=column[8],
            c_colNine=column[9],
            c_colTen=column[10],
            c_colEleven=column[11],
            c_colTwelve=column[12],
            c_colThirteen=column[13],
            c_colFourteen=column[14]

        )
    csvFileModel.objects.update_or_create(
        f_name=request.POST['csvname'],
        f_firstRow=last_row + 1,
        f_lasttRow=last_row + row
    )
    context = {}
    return render(request, template, context)
