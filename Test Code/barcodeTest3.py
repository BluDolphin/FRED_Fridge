import cv2
import pyzbar.pyzbar as pyzbar
import picamera
import picamera.array

def scan_barcode_from_webcam():
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            while True:
                # Capture frame from the camera
                camera.capture(stream, format='bgr')

                # Get the frame
                frame = stream.array

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

                # Clear the stream in preparation for the next frame
                stream.truncate(0)