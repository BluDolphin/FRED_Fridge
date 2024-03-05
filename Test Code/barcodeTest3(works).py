import cv2
from pyzbar import pyzbar
from picamera2 import Picamera2 # Picamera 1 seems to be dead ¯\_(ツ)_/¯
import time

# Function for scanning image
def readBarcode(image_path):
    # Read the image from the provided file path
    image = cv2.imread(image_path)
    # Decode barcodes from the image using pyzbar
    barcodes = pyzbar.decode(image)
    # Iterate through detected barcodes and extract data from the barcode 
    for barcode in barcodes:
        # uses UTF-8 encoding
        barcode_data = barcode.data.decode("utf-8")
        print("Barcode Data:", barcode_data)
        
        #barcode_type = barcode.type
        #print("Barcode Type:", barcode_type)

# Setup camera and configure to 4k resolution
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (3840, 2160)})
picam2.configure(camera_config)

# Take an image every second and read data
while True:
    picam2.start()
    picam2.capture_file("Barcode.jpg")
    readBarcode("Barcode.jpg")
    time.sleep(1)


"""
some code which works and shows a live preview of the camera

from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")

"""
