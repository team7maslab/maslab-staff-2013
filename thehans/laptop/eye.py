import math, Image
import cv2.cv as cv

class Eye:

    def __init__(self, debug=False):
        if debug: print "Debugging mode for vision active"
        self.camcapture = cv.CreateCameraCapture(1)
        
    def getFrame(self):
        frame = cv.QueryFrame(self.camcapture)
        return frame
    
# cyclops = Eye(debug=True)
