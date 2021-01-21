import pytesseract
import cv2
import numpy as np
import os

absolute_path = os.path.abspath(__file__+"/..")
path = absolute_path + r"/test_images/highlightedTextImg.png"
hsv = [0, 65, 59, 255, 0, 255]

pytesseract.pytesseract.tesseract_cmd = absolute_path + "/../../../AppData/Local/Tesseract-OCR/tesseract.exe"

def detectColor(img, hsv):
    #converting image to hue saturation value
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining range for highlighted colour in HSV
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    # Threshold the HSV image to get only Highlighted Color
    mask = cv2.inRange(imgHSV, lower, upper)

    # pixel values for black = 0 and white = 255
    # so bitwise_and will output non-black region of mask from image
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult

def getContours(img, imgDraw, cThr=[100, 100], minArea=1000, draw=False):
    # creating a copy of original image for drawing bounding boxs
    imgDraw = imgDraw.copy()

    # converting image to gray scale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Adding Gaussian Blur to grayscale image
    #(5,5) means kernel, it can be odd numbers only
    #if value in kernel increases bluriness will increase
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

    #Canny is used for detecting edges in image
    #to alter amount of edge detection adjust threshold1 and threshold2 parameters in Canny
    #by decreasing threshold1 and threshold2 more edges will be detected
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])

    #kernel is a matrix that we use to iterate
    #through the image in perform a function
    kernel = np.array((10, 10))

    #dilation is used to increase thickness of edge lines
    #if iterations are increased edge thickness will be furthur increased
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)

    # cv2.morphologyEx(cv2.MORPH_CLOSE) = Dilation followed by Erosion
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernel)

    #finding contours in the image and returns contours list
    #RETR_EXTERNAL it retrieves extreme outer contours
    contours, hiearchy = cv2.findContours(imgClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        #detected contours with area greater than minArea to reduce noise
        if area > minArea:

            #returns length of contour and True signifies that contour is closed
            peri = cv2.arcLength(i, True)

            #returns coordinates of the vertices of polygon by approximating the polygon
            #and True signifies that contour is closed
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)

            # if len(approx) == 4 it is a square or rectangle
            if len(approx) == 4:

                # returns the 4 points of the bounding box
                bbox = cv2.boundingRect(approx)
                finalCountours.append([len(approx), area, approx, bbox, i])
            
    # sorting based on order of highlighted text
    finalCountours = sorted(finalCountours, key=lambda x: x[3][1], reverse=False)
    if draw:
        for con in finalCountours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (255, 0, 255), 3)
    return imgDraw, finalCountours

def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append(img[y:y + h, x:x + w])
    return roiList


def roiDisplay(roiList):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(str(x),roi)

# reading image
img = cv2.imread(path)

# getting image with only highlighted text
imgResult = detectColor(img,hsv)

# getting contours of bounding box and coordinates of each highlighted text
imgContours, contours = getContours(imgResult, img, cThr=[100,150], minArea=100, draw=True)

cv2.imshow("imgContours",imgContours)

#cropping highlighted texts from original image
roiList = getRoi(img,contours)

# visualize all cropped images
# roiDisplay(roiList)

highlightedText = []
for roi in roiList:
    #extracting text from each cropped image of highlighted text 
    highlightedText.append(pytesseract.image_to_string(roi))

print("\n".join(highlightedText))

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break