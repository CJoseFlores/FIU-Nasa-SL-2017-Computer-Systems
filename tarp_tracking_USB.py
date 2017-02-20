# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.remove_contours import is_contour_bad
import time
import cv2
import imutils
import numpy as np
 
# initialize the camera by creating a VideoCapture Object.
# the ID passed is simply thy camera number (0 or -1 will be passed if only 1 camera attached.)
camera = cv2.VideoCapture(0)

# allow the camera to warmup
time.sleep(0.1)

# Create color ranges for Mask Filtering.
blueRange = (np.array([100, 110, 110]), np.array([120, 255, 255]))
yellowRange = (np.array([19, 100, 100]), np.array([39, 255, 255]))
redRange = (np.array([164, 100, 100]), np.array([184, 255, 255]))

#Initialize center variables to prevent undefined error.
cX = 1
cY = 1

# capture frames from the camera
while(True):
	# Capture the video feed frame-by-frame
	ret, image = camera.read()
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# Blur the image to help with shape recognition.
	
	blurred = cv2.GaussianBlur(resized, (21, 21), 0)

	# Convert image to HSV and make a mask for Blue, Yellow and Red.
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	threshYellow = cv2.inRange(hsv, yellowRange[0], yellowRange[1])
	threshBlue = cv2.inRange(hsv, blueRange[0], blueRange[1])
	threshRed = cv2.inRange(hsv, redRange[0], redRange[1])

	# Combine the masks.
	thresh = threshYellow + threshBlue + threshRed

	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# Remember to generalize the resolution when we move onto the PI!!!!
	badMask = np.ones((480,640,3), dtype="uint8") * 255

	# initialize the shape detector.
	sd = ShapeDetector()

	# loop over the contours
	for c in cnts:
		
		# compute the center of the contour
		M = cv2.moments(c)
		try:
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
		except ZeroDivisionError:
			# print ("Error. We dont care")
			DoNotPrint = True
		# detect the shape of the contour.
		shape = sd.detect(c)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")

		# if the contour is bad, draw it on the mask.
		if is_contour_bad(c):
			cv2.drawContours(badMask, [c], -1, 0, -1)

		# Remove the bad contours from the image.
		#image = image * badMask
		# cv2.bitwise_and(image, image, mask=badMask)

		# Draw the remaining contours and the name of the shape.
		text = "{}".format(shape)
		if not(is_contour_bad(c)):
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, text, (cX, cY),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		# show the output image
		cv2.imshow("Image", image)
		cv2.imshow("Bad Masks", badMask)
	# show the frame
	#cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

print (len(cnts))
camera.release()
cv2.destroyAllWindows()
