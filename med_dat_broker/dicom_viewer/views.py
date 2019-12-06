from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
import pydicom
import matplotlib.pyplot as plt
import pdb
import _dataarchive
import os, glob
import numpy as np
from ekg_viewer.models import ekgModel

study = [
    {
        'serie': '1',
        'patient': 'Elia Wenty',
        'picture': 'DICOM_2.JPEG'

    },
    {
        'serie': '2',
        'patient': 'Elia Wenty',
        'picture': 'DICOM_3.JPEG'

    }
]
# define global data access path
#gDatadir = "C:/Python37/meddata/_dataarchive/" if 'OS' in os.environ.keys() and os.environ['OS'].startswith('Windows') else "/var/www/meddata/_dataarchive/"
path = "_dataarchive/0002"


#dicom bild darstellen
def dicom_to_png():
#
    dir=path
    dataset = pydicom.dcmread(dir +'.DCM')
    # plot the image using matplotlib
    #dds=dataset.pixel_array
    #while len(dds.shape)>2: dds=dds[int(dds.shape[0]/2)]
    #plt.imshow(dds, cmap=plt.cm.bone)
    # plt.show()
    fig, ax = plt.subplots(1,1)

    os.system(dir+'.DCM')
    file= dir +'.DCM'
    plots = []

    for f in glob.glob(file):
        pass
        filename = f.split("/")[-1]
        ds = pydicom.dcmread(filename)
        pix = ds.pixel_array
        pix = pix*1+(-1024)
        plots.append(pix)

    y = np.dstack(plots)

    #tracker = IndexTracker(ax, y)

    #fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = buf.read()
    image = []
    image.append(image_data)
    #pdb.set_trace()
    return HttpResponse(image, content_type="image/png")

def home(request):
    context = {
        'dataLists': ekgModel.objects.values('e_recordName')
    }
    return render(request, 'dicom_viewer/home.html', context)






def detail(request,value):
    parameter = [
        {
            'recordname': value
        }
    ]
    context = {
        'list': parameter
    }
    return render(request, 'dicom_viewer/dicom_detail.html', context)



