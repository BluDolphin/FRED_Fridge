import cv2
from pyzbar import pyzbar
from picamera2 import Picamera2
picam2 = Picamera2()

def scan_barcode_from_webcam():
    # Initialize video capture from the default webcam (index 0)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Get a frame from the webcam stream
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to read frame")
            # Save the frame as an image
            cv2.imwrite('output.jpg', frame)
            break
        
        # Decode barcodes in the frame
        barcodes = pyzbar.decode(frame)

        # Process detected barcodes
        for barcode in barcodes:
            # Extract barcode data and type and print them
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            print("Barcode Data:", barcode_data)
            print("Barcode Type:", barcode_type)

        # Check for exit condition: Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release video capture and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
picam2.capture_PNG('output.png')
#while True:
#    scan_barcode_from_webcam()

