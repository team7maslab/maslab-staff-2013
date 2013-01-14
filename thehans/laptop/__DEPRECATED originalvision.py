import Image;
import cv2.cv as cv;
import numpy as np;
import math;
print "this is victors personal code. it serves no purpose."

camcapture = cv.CreateCameraCapture(1)

CHANGE_ALLOWANCE = 0.20
VICTOR_ORANGE = cv.CV_RGB(255, 102, 0)

prevFrameC = -1
prevFrameR = -1

def validBall(c, r):
    if r < 1:
        return False
    if r < 20:
        global prevFrameC
        global prevFrameR
        if prevFrameC == -1:
            prevFrameC = c
            prevFrameR = r
        changeInDist = math.sqrt(math.pow(c[0] - prevFrameC[0],2) + math.pow(c[1] - prevFrameC[1],2))
        changeInRadius = math.fabs(prevFrameR - r)
        if float(changeInRadius)/float(r) > CHANGE_ALLOWANCE:
            return False

    prevFrameC = c
    prevFrameR = r
    return True

# haar=cv.Load('/home/maslab-team7/Desktop/victorstestcode/haarcascade_frontalface_default.xml')

if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
 
while 1:
    frame = cv.QueryFrame(camcapture)
    if frame is None:
        break

    # font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) 
    # cv.PutText(frame,"Hello World!!!", (3,3),font, 255)
    
    storage = cv.CreateMemStorage()
    
    # cvSmooth(thresholded, thresholded, CV_GAUSSIAN, 9, 9)
    # circles = cvHoughCircles(thresholded, storage, CV_HOUGH_GRADIENT, 2, thresholded.height/4, 100, 40, 20, 200)
	# face detection, for funsies
    # detected = cv.HaarDetectObjects(frame, haar, storage, 1.2, 2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    # if detected:
    #	for (x,y,w,h),n in detected:
    #		cv.Rectangle(frame, (x,y), (x+w,y+h), 255)
    
    size = cv.GetSize(frame)
    
    def draw_circles(storage, output):
        circles = numpy.asarray(storage)
        for circle in circles:
              Radius, x, y = int(circle[0][3]), int(circle[0][0]), int(circle[0][4])
              cv.Circle(output, (x, y), 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
              cv.Circle(output, (x, y), Radius, cv.CV_RGB(255, 0, 0), 3, 8, 0)  
    
    hsv_frame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
    thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
    thresholded2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
    hsv_min = cv.Scalar(0, 60, 50)
    hsv_max = cv.Scalar(9, 256, 256)
    hsv_min2 = cv.Scalar(167, 50, 50)
    hsv_max2 = cv.Scalar(181, 256, 256)
    cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
    cv.InRangeS(hsv_frame, hsv_min, hsv_max, thresholded)
    cv.InRangeS(hsv_frame, hsv_min2, hsv_max2, thresholded2)
    cv.Or(thresholded, thresholded2, thresholded)
 
    # cv.Smooth(thresholded, thresholded, cv.CV_GAUSSIAN, 7, 7)
    # cv.Canny(thresholded, thresholded, 200, 500, 3)
    
    #matt = cv.CreateMat(640, 1, cv.CV_32FC3)
    # cv.HoughCircles(thresholded, matt, cv.CV_HOUGH_GRADIENT, 1, 300)
    # if matt.rows != 0:
    #    print np.asarray(matt)
    #draw_circles(storage2, hsv_frame)
    
    mat = cv.GetMat(thresholded)
    mm=cv.Moments(mat)
    if mm.m00 > 0:
        x = int(mm.m10/mm.m00)
        y = int(mm.m01/mm.m00)
        center = (x,y)
        radius = int(math.sqrt(mm.m00/math.pi)/16)
        if validBall(center,radius):
            cv.Circle(frame, center, radius, VICTOR_ORANGE, 5)
    
    # print cv.MinEnclosingCircle(mat)
    
    # contours = cv.FindContours(thresholded, storage
    # moments = cv.Moments(contours)
    # zMoment = cv.GetSpatialMoment(moments, 0, 0)
    # print moments
#        print zMoment
    # contours = cv.FindContours(thresholded, storage)
#     max_area = 0
#     print contours
#     for cnt in contours:
#     
#         area = cv.ContourArea(contours)
#         if area > max_area:
#             max_area = area
#             best_cnt = cnt
#             
    
    cv.ShowImage('Camera', frame)
    
    k=cv.WaitKey(20);
    
    
    
