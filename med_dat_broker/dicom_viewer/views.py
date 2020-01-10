import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
import io
import pydicom
import matplotlib.pyplot as plt
import pdb
import _dataarchive
import os, glob
import numpy as np
from ekg_viewer.models import ekgModel
import cv2

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
# gDatadir = "C:/Python37/meddata/_dataarchive/" if 'OS' in os.environ.keys() and os.environ['OS'].startswith('Windows') else "/var/www/meddata/_dataarchive/"
path = "_dataarchive/0002"


# dicom bild darstellen
def dicom_to_png(request):
    dataset = pydicom.dcmread('_dataarchive/0002.DCM')
    pxarr = dataset.pixel_array
    while len(pxarr.shape) > 2: pxarr = pxarr[int(pxarr.shape[0] / 2)]
    plt.imshow(pxarr, cmap=plt.cm.bone)
    # plt.show()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = buf.read()
    return HttpResponse(image_data, content_type="image/png")


def dicom_compare(request):
    pathDiff = "_dataarchive/diff.png"
    path0 = "_dataarchive/1001.jpg"
    path1 = "_dataarchive/1002.jpg"
    path2 = "_dataarchive/002.jpg"
    path3 = "_dataarchive/003.jpg"

    image1 = cv2.imread(path0)
    image2 = cv2.imread(path1)

    diffrence = cv2.subtract(image1, image2)

    Conv_hsv_Gray = cv2.cvtColor(diffrence, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # frame_b64 = base64.b64encode(mask)

    diffrence[mask != 255] = [0, 0, 255]
    image1[mask != 255] = [0, 0, 255]
    image2[mask != 255] = [0, 0, 255]

    #pdb.set_trace()
    cv2.imwrite('_dataarchive/diffOverImage1.png', image1)
    cv2.imwrite('_dataarchive/diffOverImage2.png', image2)
    cv2.imwrite(pathDiff, diffrence)

    # maskEncode = base64.b64encode(mask)


    #diffencoded = base64.b64encode(open(pathDiff, "rb").read())
    buffer = cv2.imencode('.png', diffrence)[1].tostring()
    #frame_b64 = base64.b64encode(buffer)
    diffencoded = base64.b64encode(buffer).decode()
    imgStr = 'data:image/png;base64,{}'.format(diffencoded)


    # images = []
    print(diffencoded)
    # return HttpResponse(images, content_type="image/jpg")
    return render(request, 'dicom_viewer/vergleich.html', {'img': imgStr})


def home(request):
    context = {
        'dataLists': ekgModel.objects.values('e_recordName')
    }
    return render(request, 'dicom_viewer/home.html', context)


def detail(request, value):
    dataset = pydicom.dcmread('_dataarchive/0002.DCM')
    patient_name = dataset.PatientName
    patient_display_name = patient_name.family_name + ", " + patient_name.given_name
    slicelocation = dataset.get('SliceLocation',
                                "(missing)")  # get verwenden wenn mann nicht sicher ist ob der wert befüllt ist und man einen ersatz haben will
    pixelspacing = dataset.get('SliceLocation', "(missing)")
    rows = dataset.get('Rows', "(missing)")
    cols = dataset.get('Columns', "(missing)")
    if 'PixelData' in dataset:
        size = str(len(dataset.PixelData)) + " bytes"
    elif 'Rows' in dataset:
        size = str(rows * cols) + "px"
    else:
        size = "(missing)"
    parameter = [
        {
            'filename': value,
            'storagetype': dataset.SOPClassUID,
            'studydate': dataset.StudyDate,
            'patientid': dataset.PatientID,
            'modality': dataset.Modality,
            'patientdisplayname': patient_display_name,
            'rows': rows,
            'cols': cols,
            'size': size,
            'pixelspacing': pixelspacing,
            'slicelocation': slicelocation
        }
    ]
    context = {
        'list': parameter
    }
    return render(request, 'dicom_viewer/dicom_detail.html', context)


def dicom_comparison(request, value):
    value = value + ","
    value += request.POST.get('textfield', None)
    parameter = []
    record_names = value.split(",")
    for value in record_names:
        dataset = pydicom.dcmread('_dataarchive/0002.DCM')
        patient_name = dataset.PatientName
        patient_display_name = patient_name.family_name + ", " + patient_name.given_name
        slicelocation = dataset.get('SliceLocation',
                                    "(missing)")  # get verwenden wenn mann nicht sicher ist ob der wert befüllt ist und man einen ersatz haben will
        pixelspacing = dataset.get('SliceLocation', "(missing)")
        rows = dataset.get('Rows', "(missing)")
        cols = dataset.get('Columns', "(missing)")
        if 'PixelData' in dataset:
            size = str(len(dataset.PixelData)) + " bytes"
        elif 'Rows' in dataset:
            size = str(rows * cols) + "px"
        else:
            size = "(missing)"
        parameter.append(
            {
                'filename': value,
                'storagetype': dataset.SOPClassUID,
                'studydate': dataset.StudyDate,
                'patientid': dataset.PatientID,
                'modality': dataset.Modality,
                'patientdisplayname': patient_display_name,
                'rows': rows,
                'cols': cols,
                'size': size,
                'pixelspacing': pixelspacing,
                'slicelocation': slicelocation
            })

    context = {
        'list': parameter
    }
    return render(request, 'dicom_viewer/dicom_comparison.html', context)
