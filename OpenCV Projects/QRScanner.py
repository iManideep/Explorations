import cv2
import numpy as np
from pyzbar.pyzbar import decode
# To capture a video, you need to create a VideoCapture object. 
# Its argument can be either the device index or the name of a video file. 
# Device index is just the number to specify which camera.
cap = cv2.VideoCapture(0)
#3 and 4 are numbers set by opencv to width and height respectively
cap.set(3,640)
cap.set(4,480)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        # barcode.polygon gives coordinates of QR in the image
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        # creating a box around QR using coordinates
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        #adding text extracted from QR above top-left of box created around QR
        cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
    #show image in new window named as Result
    cv2.imshow('Result',img)
    #waitKey(0) will pause your screen because it will wait infinitely for keyPress on your keyboard 
    #and will not refresh the frame(cap.read()) using your WebCam. 
    #waitKey(1) will wait for keyPress for just 1 millisecond and it will continue to refresh and 
    #read frame from your webcam using cap.read().
    #waitKey returns a 32-bit integer corresponding to the pressed key
    #The 0xFF in this scenario is representing binary 11111111 a 8 bit binary, 
    #since we only require 8 bits to represent a character we AND waitKey(0) to 0xFF. 
    # As a result, an integer is obtained below 255.
    #Press "q" to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# release the video capture object
cap.release()
#close the opencv window named as Result
cv2.destroyWindow('Result')