import cv2
from pyzbar import pyzbar

def scan_barcode_from_image(image_path):
    # Read the image from the provided file path
    image = cv2.imread(image_path)
    # Decode barcodes from the image using pyzbar
    barcodes = pyzbar.decode(image)
    # Iterate through detected barcodes and extract data from the barcode 
    for barcode in barcodes:
        # uses UTF-8 encoding
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print("Barcode Data:", barcode_data)
        print("Barcode Type:", barcode_type)

scan_barcode_from_image("testBarcode.jpg")