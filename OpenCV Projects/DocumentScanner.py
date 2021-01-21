import cv2
import numpy as np
import os

absolute_path = os.path.abspath(__file__+"/..")
path = absolute_path + r"/test_images/document_scanner.jpg"
widthImg  = 480
heightImg = 640
#kernel is a matrix that we use to iterate
#through the image in perform a function
kernel = np.ones((5, 5))

def preprocessing(img):
    
    #converting resized image to gray scale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Adding Gaussian Blur to grayscale image
    #(3,3) means kernel, it can be odd numbers only
    #if value in kernel increases bluriness will increase
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    #Canny is used for detecting edges in image
    #to alter amount of edge detection adjust threshold1 and threshold2 parameters in Canny
    #by decreasing threshold1 and threshold2 more edges will be detected
    imgCanny = cv2.Canny(imgBlur,220,230)
    
    #dilation is used to increase thickness of edge lines
    #if iterations are increased edge thickness will be furthur increased
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    
    #erosion is used to decrease thickness of edge lines
    #if iterations are increased edge thickness will be furthur decreased
    imgEros = cv2.erode(imgDial, kernel, iterations=1)
    cv2.imshow("Preprocessed Image",imgEros)
    
    return imgEros

def getBiggestContour(preprocessedImg,imgContours):
    
    #finding contours in the image and returns contours list
    #RETR_EXTERNAL it retrieves extreme outer contours
    contours, hierarchy = cv2.findContours(preprocessedImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw all detected contours
    cv2.drawContours(imgContours, contours, -1, (0, 0, 255), 10)
    cv2.imshow("Detected Contours",imgContours)
    
    #to find out biggest contour by checking its area
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        
        #detected contours with area greater than 5,000 to reduce noise
        if area > 5000:
            
            #returns length of contour and True signifies that contour is closed
            peri = cv2.arcLength(contour, True)
            
            #returns coordinates of the vertices of polygon by approximating the polygon
            #and True signifies that contour is closed
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            #if len(approx)==4 it is a square or rectangle
            if area > max_area and len(approx) == 4:
                biggest_contour=contour
                biggest = approx
                max_area = area
                
    #returning vertices of polygon and its area
    return biggest

def reorder(myPoints):
    #creating empty numpy array with dimensions of myPoints
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    
    #reshaping from 4x1x2 to 4x2
    myPoints = myPoints.reshape((4, 2))
    
    #returns array of sum of the each point x and y co-ordinates
    add = myPoints.sum(1)
    
    #origin will be at top-left corner of image
    #for top-left corner point of page in image sum of its x and y co-ordinates will be minimum
    #so myPoints[np.argmin(add)] will return it
    myPointsNew[0] = myPoints[np.argmin(add)]
    
    #for bottom-right corner point of page in image sum of its x and y co-ordinates will be maximum
    #so myPoints[np.argmax(add)] will return it
    myPointsNew[3] =myPoints[np.argmax(add)]
    
    #returns array of difference between the each point y and x co-ordinates
    diff = np.diff(myPoints, axis=1)
    
    #for top-right corner point of page in image difference between its y and x co-ordinates will be minimum
    #so myPoints[np.argmin(diff)] will return it
    myPointsNew[1] =myPoints[np.argmin(diff)]
    
    #for bottom-left corner point of page in image difference between its y and x co-ordinates will be maximum
    #so myPoints[np.argmax(diff)] will return it
    myPointsNew[2] = myPoints[np.argmax(diff)]
    
    return myPointsNew

#reading original image
img=cv2.imread(path)

#resizing original image
img=cv2.resize(img,(widthImg,heightImg))

#to draw all counters creating a copy
imgContours = img.copy()
#to plot polygon vertices of biggest contour creating a copy
imgBigContourPoints = img.copy()

#preprocessing image
preprocessedImg = preprocessing(img)

#extracted biggest contour from pre-processed image
biggest = getBiggestContour(preprocessedImg,imgContours)

if biggest.size != 0:

    #reordering co-ordinates
    biggest=reorder(biggest)

    # plot vertices of polygon
    cv2.drawContours(imgBigContourPoints, biggest, -1, (0, 255, 0), 20)
    cv2.imshow("Page Corner Points",imgBigContourPoints)

    # Prepare points for wrap by converting integers to float
    #pts1 is actual view of page in imageq
    pts1 = np.float32(biggest)
    #pts2 is perspective of page in image which we want
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])
    #get perspective transformation from pts1 to pts2
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    #remove 20 pixels from each side
    imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
    #resizing image after removing pixels
    imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))
    cv2.imshow("Changed Image Perspective",imgWarpColored)

    # APPLY ADAPTIVE THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    #to get binary image
    imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
    #from black to white & white to black (0 to 1, 1to 0)
    imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
    #adding median blur to remove noise
    imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
    cv2.imshow("Processed Image",imgAdaptiveThre)
    
while True:
    #press q to close all image tabs opened
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #press s to save process image
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print("Saved")
        cv2.imwrite("Scanned/Processed_"+path,imgAdaptiveThre)
        
cv2.destroyAllWindows()