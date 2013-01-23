import math, Image
import cv2.cv as cv
import numpy

class Eye:

    VICTOR_ORANGE = cv.CV_RGB(255, 102, 0)
    FRAME_WIDTH = 160
    FRAME_HEIGHT = 120
    RED_HSV_MIN = cv.Scalar(0, 60, 50)
    RED_HSV_MAX = cv.Scalar(9, 256, 256)
    RED_HSV_MIN2 = cv.Scalar(167, 50, 50)
    RED_HSV_MAX2 = cv.Scalar(181, 256, 256)
    
    GREEN_HSV_MIN = cv.Scalar(100, 50, 20)
    GREEN_HSV_MAX = cv.Scalar(110, 255, 255)
    GREEN_HSV_MIN2 = cv.Scalar(60, 50, 20)
    GREEN_HSV_MAX2 = cv.Scalar(70, 255, 255)

    YELLOW_HSV_MIN = cv.Scalar(20, 100, 100)
    YELLOW_HSV_MAX = cv.Scalar(30, 255, 255)
    YELLOW_HSV_MIN2 = cv.Scalar(35, 100, 100)
    YELLOW_HSV_MAX2 = cv.Scalar(31, 255, 255)

    PURPLE_HSV_MIN = cv.Scalar(200, 50, 70)
    PURPLE_HSV_MAX = cv.Scalar(205, 255, 255)
    PURPLE_HSV_MIN2 = cv.Scalar(215, 50, 70)
    PURPLE_HSV_MAX2 = cv.Scalar(216, 255, 255)

##    CYAN_HSV_MIN = cv.Scalar(100, 70, 50)
##    CYAN_HSV_MAX = cv.Scalar(105, 255, 255)
##    CYAN_HSV_MIN2 = cv.Scalar(140, 60, 50)
##    CYAN_HSV_MAX2 = cv.Scalar(165, 255, 255)    

    CYAN_HSV_MIN = cv.Scalar(95, 176, 115)
    CYAN_HSV_MAX = cv.Scalar(108, 255, 255)
    CYAN_HSV_MIN2 = cv.Scalar(120, 176, 115)
    CYAN_HSV_MAX2 = cv.Scalar(125, 255, 255)    
    
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug: print "Debugging mode for vision active"
        self.camcapture = cv.CreateCameraCapture(1)
    
    # fetches one frame from the camera
    def getFrame(self):
        frame = cv.QueryFrame(self.camcapture)
        thumbnail = cv.CreateImage((self.FRAME_WIDTH,self.FRAME_HEIGHT), frame.depth, frame.nChannels)
        cv.Resize(frame, thumbnail, cv.CV_INTER_AREA)
        frame = thumbnail
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
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        cv.InRangeS(hsv_frame, self.RED_HSV_MIN, self.RED_HSV_MAX, thresholded)
        cv.InRangeS(hsv_frame, self.RED_HSV_MIN2, self.RED_HSV_MAX2, thresholded2)
        cv.Or(thresholded, thresholded2, thresholded)
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            # red ball not found. will implement method later.
            x = 0
            y = 0
        center = (x,y)
        radius = int(math.sqrt(mm.m00/math.pi)/16)
        
        # temporarily disable validball checker
        # if validBall(center,radius):
        # cv.Circle(thresholded, center, radius, self.VICTOR_ORANGE, 5)
        
        # calculate the relative position of the ball with 0,0 being the center of the frame. tuple of values between -1 and 1
        if self.debug: print "Center of the red ball is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        if self.debug: print "Relative Center is: " + str(relativeCenter)

        return relativeCenter, thresholded

    # fetch the coordinates of the greenball relative to the center and the frame
    def findGreenBall(self, frame):
        """takes in a frame capture of the camera and returns a thresholded frame"""
        
        size = cv.GetSize(frame)
        hsv_frame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
        thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        thresholded2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        cv.InRangeS(hsv_frame, self.GREEN_HSV_MIN, self.GREEN_HSV_MAX, thresholded)
        cv.InRangeS(hsv_frame, self.GREEN_HSV_MIN2, self.GREEN_HSV_MAX2, thresholded2)
        cv.Or(thresholded, thresholded2, thresholded)
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            # red ball not found. will implement method later.
            x = 0
            y = 0
        center = (x,y)
        radius = int(math.sqrt(mm.m00/math.pi)/16)
        
        # temporarily disable validball checker
        # if validBall(center,radius):
        # cv.Circle(thresholded, center, radius, self.VICTOR_ORANGE, 5)
        
        # calculate the relative position of the ball with 0,0 being the center of the frame. tuple of values between -1 and 1
        if self.debug: print "Center of the green ball is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        if self.debug: print "Relative Center is: " + str(relativeCenter)

        return relativeCenter, thresholded

    # fetch the coordinates of the yellow wall relative to the center and the frame
    def findYellowWall(self, frame):
        """takes in a frame capture of the camera and returns a thresholded frame"""
        
        size = cv.GetSize(frame)
        hsv_frame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
        thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        thresholded2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        cv.InRangeS(hsv_frame, self.YELLOW_HSV_MIN, self.YELLOW_HSV_MAX, thresholded)
        cv.InRangeS(hsv_frame, self.YELLOW_HSV_MIN2, self.YELLOW_HSV_MAX2, thresholded2)
        cv.Or(thresholded, thresholded2, thresholded)
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            # red ball not found. will implement method later.
            x = 0
            y = 0
        center = (x,y)
        
        if self.debug: print "Center of yellow moment is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        if self.debug: print "Relative Center is: " + str(relativeCenter)

        return relativeCenter, thresholded

    # fetch the coordinates of the yellow wall relative to the center and the frame
    def findPurpleTower(self, frame):
        """takes in a frame capture of the camera and returns a thresholded frame"""
        
        size = cv.GetSize(frame)
        hsv_frame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
        thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        thresholded2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        cv.InRangeS(hsv_frame, self.PURPLE_HSV_MIN, self.PURPLE_HSV_MAX, thresholded)
        cv.InRangeS(hsv_frame, self.PURPLE_HSV_MIN2, self.PURPLE_HSV_MAX2, thresholded2)
        cv.Or(thresholded, thresholded2, thresholded)
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            # red ball not found. will implement method later.
            x = 0
            y = 0
        center = (x,y)
        
        if self.debug: print "Center of yellow moment is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        if self.debug: print "Relative Center is: " + str(relativeCenter)

        return relativeCenter, thresholded

    # fetch the coordinates of the button relative to the center and the frame
    def findCyanButton(self, frame):
        """takes in a frame capture of the camera and returns a thresholded frame"""
        
        size = cv.GetSize(frame)
        hsv_frame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
        thresholded = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        thresholded2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        cv.InRangeS(hsv_frame, self.CYAN_HSV_MIN, self.CYAN_HSV_MAX, thresholded)
        cv.InRangeS(hsv_frame, self.CYAN_HSV_MIN2, self.CYAN_HSV_MAX2, thresholded2)
        cv.Or(thresholded, thresholded2, thresholded)
        
        # calculate the center and the radius based on the moment
        mat = cv.GetMat(thresholded)
        mm=cv.Moments(mat)
        if mm.m00 > 0:
            x = int(mm.m10/mm.m00)
            y = int(mm.m01/mm.m00)
        else:
            # red ball not found. will implement method later.
            x = 0
            y = 0
        center = (x,y)
        radius = int(math.sqrt(mm.m00/math.pi)/16)
        
        # temporarily disable validball checker
        # if validBall(center,radius):
        # cv.Circle(thresholded, center, radius, self.VICTOR_ORANGE, 5)
        
        # calculate the relative position of the ball with 0,0 being the center of the frame. tuple of values between -1 and 1
        if self.debug: print "Center of the red ball is: " + str(center)
        relativeCenterX = (float(x)-float(self.FRAME_WIDTH)/2) / (float(self.FRAME_WIDTH)/2)
        relativeCenterY = (float(y)-float(self.FRAME_HEIGHT)/2) / (float(self.FRAME_HEIGHT)/2)
        relativeCenter = (relativeCenterX, relativeCenterY)
        if self.debug: print "Relative Center is: " + str(relativeCenter)

        return relativeCenter, thresholded


    # opens a new window with the image
    def showImage(self, frame):
        """debugging tool for outputting the frame as a new window"""
        cv.ShowImage('Camera', frame)    
        cv.WaitKey(20)

    def kill(self):
        cv.DestroyAllWindows()

##d = Eye(True)
##while True:
##    f = d.getFrame()
##    center, q = d.findRedBall(f)
##    d.showImage(q)
##    cv.WaitKey(10)
