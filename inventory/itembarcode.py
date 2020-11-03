import barcode
import random
import pickle
import os
from InvApp.settings import TEMPFILES_FOLDER, TEMPIMGS_FOLDER, MEDIA_ROOT
from datetime import datetime
from barcode.writer import ImageWriter


def getBarcode():

    bcodes = []

    with open(TEMPFILES_FOLDER+'/bcodes.pkl', 'rb') as f:
        bcodes = pickle.load(f)

    while True:
        num = random.randint(1000000000000, 9999999999999)
        if num not in bcodes:
            break
        continue

    return str(num)


def makeBarcodeIMG(code, item_name):
    bcodes = []

    with open(TEMPFILES_FOLDER+'/bcodes.pkl', 'rb') as f:
        bcodes = pickle.load(f)

    bcodes.append(code)

    with open(TEMPFILES_FOLDER+'/bcodes.pkl', 'wb') as f:
        pickle.dump(bcodes, f)

    ean = barcode.get('ean13', str(code), writer=ImageWriter())

    filename = ean.save(os.path.join(MEDIA_ROOT,
                                     'barcodes/' + item_name + "_" + str(ean.get_fullcode()))
                        )
    return ean.get_fullcode()
