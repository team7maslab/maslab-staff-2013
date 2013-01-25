# aka balloon3run_video.py
# detects multiple balls per frame
# NO MORE blossoming effect when ball crosses ROI
# add emergency code halving ROI in case of no balls detected?
# still improper radius approx in case when red around frame borders


import cv
import math

class thresholding:
    def __init__(self, image):
        self.image = image
        self.gray = cv.CreateImage(cv.GetSize(image), 8, 1)   # initial image processing
        self.thresh = 98
        self.max_thresh = 255

        self.size = cv.GetSize(image)

##        ## green
##        self.h1 = 140
##        self.s1 = 80
##        self.v1 = 0
##        self.h2 = 145
##        self.s2 = 55
##        self.v2 = 255
##        self.h3 = 50
##        self.s3 = 50
##        self.v3 = 20
##        self.h4 = 80
##        self.s4 = 255
##        self.v4 = 255

        ## yellow
        self.h1 = 20
        self.s1 = 100
        self.v1 = 100
        self.h2 = 30
        self.s2 = 255
        self.v2 = 255
        self.h3 = 30
        self.s3 = 100
        self.v3 = 100
        self.h4 = 31
        self.s4 = 255
        self.v4 = 255

        self.HSV_MIN = cv.Scalar(self.h1, self.s1, self.v1)
        self.HSV_MAX = cv.Scalar(self.h2, self.s2, self.v2)
        self.HSV_MIN2 = cv.Scalar(self.h3, self.s3, self.v3)
        self.HSV_MAX2 = cv.Scalar(self.h4, self.s4, self.v4)

        self.thresholded = cv.CreateImage(self.size, cv.IPL_DEPTH_8U, 1)
        self.thresholded2 = cv.CreateImage(self.size, cv.IPL_DEPTH_8U, 1)
        self.hsv_frame = cv.CreateImage(self.size, cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(self.image, self.hsv_frame, cv.CV_BGR2HSV)

    def show(self):
        cv.InRangeS(self.hsv_frame, self.HSV_MIN, self.HSV_MAX, self.thresholded)
        cv.InRangeS(self.hsv_frame, self.HSV_MIN2, self.HSV_MAX2, self.thresholded2)
        cv.Or(self.thresholded, self.thresholded2, self.thresholded)

        cv.ShowImage("camera", self.thresholded)
        cv.WaitKey(10)

        
    def h1_callback(self, h1):
        self.h1 = h1
        self.HSV_MIN = cv.Scalar(self.h1, self.s1, self.v1)
        self.show()

    def h2_callback(self, h2):
        self.h2 = h2
        self.HSV_MAX = cv.Scalar(self.h2, self.s2, self.v2)
        self.show()

    def h3_callback(self, h3):
        self.h3 = h3
        self.HSV_MIN2 = cv.Scalar(self.h3, self.s3, self.v3)
        self.show()

    def h4_callback(self, h4):
        self.h4 = h4
        self.HSV_MAX2 = cv.Scalar(self.h4, self.s4, self.v4)
        self.show()
        
    def run(self):
        
        # show image
        cv.CvtColor(self.image, self.image, cv.CV_BGR2HSV)
        cv.CreateTrackbar("H1", "camera", self.h1, self.max_thresh, self.h1_callback)
        cv.CreateTrackbar("H2", "camera", self.h2, self.max_thresh, self.h2_callback)
        cv.CreateTrackbar("H3", "camera", self.h3, self.max_thresh, self.h3_callback)
        cv.CreateTrackbar("H4", "camera", self.h3, self.max_thresh, self.h4_callback)
        
        self.HSV_MIN = cv.Scalar(self.h1, self.s1, self.v1)
        self.HSV_MAX = cv.Scalar(self.h2, self.s2, self.v2)
        self.HSV_MIN2 = cv.Scalar(self.h3, self.s3, self.v3)
        self.HSV_MAX2 = cv.Scalar(self.h4, self.s4, self.v4)

        cv.InRangeS(self.hsv_frame, self.HSV_MIN, self.HSV_MAX, self.thresholded)
        cv.InRangeS(self.hsv_frame, self.HSV_MIN2, self.HSV_MAX2, self.thresholded2)
        cv.Or(self.thresholded, self.thresholded2, self.thresholded)

        # show image
        cv.ShowImage("camera", self.thresholded)
        cv.WaitKey(10)


        cv.WaitKey()


if __name__ == "__main__":
    try:
        while True:
            image = cv.LoadImage("tower.jpg")
            thresholding(image).run()
            cv.WaitKey(1000)
            print

    except KeyboardInterrupt:
        cv.DestroyAllWindows()
