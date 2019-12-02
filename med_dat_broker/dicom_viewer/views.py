from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
import pydicom
import matplotlib.pyplot as plt
import pdb
import _dataarchive
import os
import wfdb


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
    dir=path
    dataset = pydicom.dcmread(dir +'.DCM')
    # plot the image using matplotlib
    dds=dataset.pixel_array
    while len(dds.shape)>2: dds=dds[int(dds.shape[0]/2)]
    plt.imshow(dds, cmap=plt.cm.bone)
    # plt.show()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = buf.read()
    image = []
    image.append(image_data)
    pdb.set_trace()
    return HttpResponse(image, content_type="image/png")

def home(request):
    context = {
        'studies': study,
        'pictures' : dicom_to_png()
    }
    return render(request, 'dicom_viewer/home.html', context)

def about(request):
    return HttpResponse('<h1>DCM About</h1>')



