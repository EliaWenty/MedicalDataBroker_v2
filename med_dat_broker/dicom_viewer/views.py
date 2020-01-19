import base64
import io
import pdb

import cv2
import matplotlib.pyplot as plt
import pydicom
from PIL import Image, ImageEnhance
from django.http import HttpResponse
from django.shortcuts import render
from pydicom._storage_sopclass_uids import CTImageStorage
from pydicom.dataset import Dataset
import numpy as np

from pynetdicom import (
    AE, evt, build_role,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

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
# gDatadir = "C:/Python37/meddata/_dataarchive/" if 'OS' in os.environ.keys() and os.environ['OS'].startswith('Windows') else "/var/www/meddata/_dataarchive/"
path = "_dataarchive/0002"
PACS_HOST = "pacs.spengergasse.at"
PACS_PORT = 11112
PACS_AE = "DCM4CHEE"
QUERYRETRIEVELEVEL = 'IMAGE'
LOCALARCHIVE = "_dataarchive/"


# dicom bild darstellen
def dicom_to_png(request):
    dataset = dicom_retrieve(0, 0, 0, 0, '0002') #insert model fields
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
    path1 = "_dataarchive/1001.jpg"
    path2 = "_dataarchive/1002.jpg"

    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)

    diffrence = cv2.subtract(image1, image2)

    Conv_hsv_Gray = cv2.cvtColor(diffrence, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # frame_b64 = base64.b64encode(mask)

    diffrence[mask != 255] = [0, 0, 255]
    image1[mask != 255] = [0, 0, 255]
    image2[mask != 255] = [0, 0, 255]

    # cv2.imwrite('_dataarchive/diffOverImage1.png', image1)
    # cv2.imwrite('_dataarchive/diffOverImage2.png', image2)
    # cv2.imwrite(pathDiff, diffrence)

    image1OG = cv2.imread(path1)
    image2OG = cv2.imread(path2)

    images = [diffrence, image1, image2, image1OG, image2OG]
    imagesEnc = []
    # imageDic = {}
    for i in range(len(images)):
        buffer = cv2.imencode('.png', images[i])[1].tostring()
        diffencoded = base64.b64encode(buffer).decode()
        imgStr = 'data:image/png;base64,{}'.format(diffencoded)
        # imageDic['id']
        imagesEnc.append(imgStr)

    imageEnc1 = imagesEnc[0]
    imageEnc2 = imagesEnc[1]
    imageEnc3 = imagesEnc[2]
    imageEnc4 = imagesEnc[3]
    imageEnc5 = imagesEnc[4]
    #print(imageEnc5)
    #pdb.set_trace()

    imgList = [

        {
            'id': 1,
            'img': imageEnc1,
        }, {
            'id': 2,
            'img': imageEnc2,
        }, {
            'id': 3,
            'img': imageEnc3,
        }, {
            'id': 4,
            'img': imageEnc4,
        }, {
            'id': 5,
            'img': imageEnc5,
        },
    ]
    contextImg = {
        'imgList' : imgList
    }
    # return HttpResponse(images, content_type="image/jpg")
    return render(request, 'dicom_viewer/vergleich.html', contextImg)


def home(request):
    context = {
        'dataLists': ekgModel.objects.values('e_recordName')
    }
    return render(request, 'dicom_viewer/home.html', context)


def detail(request, value):
   # try:
        dataset = dicom_retrieve(0, 0, 0, 0, '0002') #insert model fields
        patient_name = dataset.PatientName
        patient_display_name = patient_name.family_name + ", " + patient_name.given_name
        slicelocation = dataset.get('SliceLocation', "(missing)")  # get verwenden wenn mann nicht sicher ist ob der wert befüllt ist und man einen ersatz haben will
        pixelspacing = dataset.get('SliceLocation', "(missing)")
        rows = dataset.get('Rows', "(missing)")
        cols = dataset.get('Columns', "(missing)")

        pxarr = dataset.pixel_array
        while len(pxarr.shape) > 2: pxarr = pxarr[int(pxarr.shape[0] / 2)]
        plt.imshow(pxarr, cmap=plt.cm.bone)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image_data = buf.read()

        img = Image.open(io.BytesIO(image_data))
        imgContrast = Image.open(io.BytesIO(image_data))
        enhancer = ImageEnhance.Contrast(imgContrast)
        enh_imgContrastArr = []
        contrasValArr = []
        for i in range(-6, 6):
            contrasValArr.append(i/2)
            enh_imgContrastArr.append(enhancer.enhance(i/2))


        imgStrArr = []
        for i in range(len(enh_imgContrastArr)):
            imgNPArr = np.array(enh_imgContrastArr[i])
            buffer = cv2.imencode('.png', imgNPArr)[1].tostring()
            imgdecoded = base64.b64encode(buffer).decode()
            imgStr = 'data:image/png;base64,{}'.format(imgdecoded)
            imgStrArr.append(imgStr)


        imgNPArr = np.array(img)
        buffer = cv2.imencode('.png', imgNPArr)[1].tostring()
        imgdecoded = base64.b64encode(buffer).decode()
        imgStrpng = 'data:image/png;base64,{}'.format(imgdecoded)


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
        images = [
            {
                'image' : imgStrpng
            }
        ]
        contrast_images = [
        ]
        for i in range(len(imgStrArr)):
            contrast_images.append({'values' : contrasValArr[i-1],
                                    'pic': imgStrArr[i-1]})

        context = {
            'list': parameter,
            'list_img' : images,
            'list_con_img' : contrast_images
        }

        return render(request, 'dicom_viewer/dicom_detail.html', context)
    #except:
        #return HttpResponse("Could not retrieve DICOM", content_type="text/plain")


def dicom_comparison(request, value):
    value = value + ","
    value += request.POST.get('textfield', None)
    parameter = []
    record_names = value.split(",")
    for value in record_names:
        dataset = pydicom.dcmread('_dataarchive/0002.DCM')
        patient_name = dataset.PatientName
        patient_display_name = patient_name.family_name + ", " + patient_name.given_name
        slicelocation = dataset.get('SliceLocation', "(missing)")  # get verwenden wenn mann nicht sicher ist ob der wert befüllt ist und man einen ersatz haben will
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

def dicom_download(request, value, format='png'):
    if format == 'png':
        dataset = dicom_retrieve(0, 0, 0, 0, '0002') #insert model fields
        rows = dataset.get('Rows', "(missing)")
        cols = dataset.get('Columns', "(missing)")
        pxarr = dataset.pixel_array
        while len(pxarr.shape) > 2: pxarr = pxarr[int(pxarr.shape[0] / 2)]
        plt.imshow(pxarr, cmap=plt.cm.bone)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image_data = buf.read()
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=%s.png' % value
        img = Image.open(io.BytesIO(image_data))
        img.save(response, 'png')
        return response
    else:
        return HttpResponse("Format not supported!", content_type="text/plain")



def dicom_retrieve(patientid, studyid, seriesid, imageid, sopinstanceuid):
    dataset = "null"
    #check if file in local directory
    try:
        dataset = pydicom.dcmread(LOCALARCHIVE+sopinstanceuid+".DCM")
    except:
        # Implement the handler for evt.EVT_C_STORE
        def handle_store(event):
            """Handle a C-STORE request event."""
            ds = event.dataset
            context = event.context

            # Add the DICOM File Meta Information
            meta = Dataset()
            meta.MediaStorageSOPClassUID = ds.SOPClassUID
            meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
            meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
            meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
            meta.TransferSyntaxUID = context.transfer_syntax

            # Add the file meta to the dataset
            ds.file_meta = meta

            # Set the transfer syntax attributes of the dataset
            ds.is_little_endian = context.transfer_syntax.is_little_endian
            ds.is_implicit_VR = context.transfer_syntax.is_implicit_VR

            #keep the dataset to return later
            dataset = ds

        handlers = [(evt.EVT_C_STORE, handle_store)]

        # Initialise the Application Entity
        ae = AE()

        # Add the requested presentation contexts (QR SCU)
        ae.add_requested_context('1.2.840.10008.5.1.4.1.2.1.3') #Patient get
        # Add the requested presentation context (Storage SCP)
        ae.add_requested_context(CTImageStorage)

        # Create an SCP/SCU Role Selection Negotiation item for CT Image Storage
        role = build_role(CTImageStorage, scp_role=True)

        # Create our Identifier (query) dataset
        # We need to supply a Unique Key Attribute for each level above the
        #   Query/Retrieve level
        ds = Dataset()
        ds.QueryRetrieveLevel = QUERYRETRIEVELEVEL
        # Unique key for PATIENT level
        ds.PatientID = patientid
        # Unique key for STUDY level
        ds.StudyInstanceUID = studyid
        # Unique key for SERIES level
        ds.SeriesInstanceUID = seriesid
        # Unique key for IMAGE level
        ds.ImageInstanceUID = imageid

        # Associate with peer AE at IP 127.0.0.1 and port 11112
        assoc = ae.associate(PACS_HOST, PACS_PORT, ext_neg=[role], evt_handlers=handlers)

        if assoc.is_established:
            # Use the C-GET service to send the identifier
            responses = assoc.send_c_get(ds, '1.2.840.10008.5.1.4.1.2.1.3')

            for (status, identifier) in responses:
                if status:
                    print('C-GET query status: 0x{0:04x}'.format(status.Status))

                    # If the status is 'Pending' then `identifier` is the C-GET response
                    if status.Status in (0xFF00, 0xFF01):
                        print(identifier)
                else:
                    print('Connection timed out, was aborted or received invalid response')

            # Release the association
            assoc.release()
        else:
            print('Association rejected, aborted or never connected')
    return dataset
