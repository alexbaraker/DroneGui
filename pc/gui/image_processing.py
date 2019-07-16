#######################################################################################################################################
#   By: SupremeDrones Team; Alex Baraker, Dean, Kelsey, Hammad
#   Date: 3/06/2019
#   Info: Image processing class for detecting colored balls
#######################################################################################################################################

from collections import deque
import cv2
import sys
import numpy as np
import imutils


class image_processing():


    # Thanks: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    @staticmethod
    def detect_circle(cv_img, color_filter=None):
        centerx, centery, radius = None, None, None
        upper = (14, 255, 255)
        lower = (0, 200, 0)

        blurred = cv2.GaussianBlur(cv_img, (11, 11), 0)
        hsv     = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
        # construct a mask for the color "orange", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # find contours in the mask and initialize the current (x, y) center of the ball
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
    
        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            centroid = max(contours, key=cv2.contourArea)
            ((centerx, centery), radius) = cv2.minEnclosingCircle(centroid)

            centerx = int(centerx)
            centery = int(centery)
            radius  = int(radius)

        return centerx, centery, radius