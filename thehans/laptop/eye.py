import math, Image
import cv2.cv as cv

class Eye:

    VICTOR_ORANGE = cv.CV_RGB(255, 102, 0)
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug: print "Debugging mode for vision active"
        self.camcapture = cv.CreateCameraCapture(1)
    
    # fetches one frame from the camera
    def getFrame(self):
        frame = cv.QueryFrame(self.camcapture)
        if frame is None:
            print "Error in getting frame"
        return frame
    
    # fetch the coordinates of the redball relative to the center and the frame
    def findRedBall(self, frame):
        """takes in a frame capture of the camera and returns a thresholded frame"""
        
        size = cv.GetSize(frame)
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
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            x = 0
            y = 0
        center = (x,y)
        radius = int(math.sqrt(mm.m00/math.pi)/16)
        
        # temporarily disable validball checker
        # if validBall(center,radius):
        cv.Circle(thresholded, center, radius, self.VICTOR_ORANGE, 5)
        
        # calculate the relative position of the ball with 0,0 being the center of the frame. tuple of values between -1 and 1
        if self.debug: print "Center of the red ball is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        
        return relativeCenter, thresholded
    
    # opens a new window with the image
    def showImage(self, frame):
        """debugging tool for outputting the frame as a new window"""
        cv.ShowImage('Camera', frame)    
        cv.WaitKey(10)



