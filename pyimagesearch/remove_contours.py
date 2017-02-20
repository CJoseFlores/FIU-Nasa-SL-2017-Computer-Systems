# USAGE
# python remove_contours.py

# import the necessary packages
import numpy as np
import cv2

def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4