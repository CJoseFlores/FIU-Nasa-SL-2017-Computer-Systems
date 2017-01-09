# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import time
import cv2
import imutils
 
# initialize the camera by creating a VideoCapture Object.
# the ID passed is simply thy camera number (0 or -1 will be passed if only 1 camera attached.)
camera = cv2.VideoCapture(0)

# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
while(True):
	# Capture the video feed frame-by-frame
	ret, image = camera.read()

	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()

	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		try:
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
		except ZeroDivisionError:
			print("Error. I dont care")
		shape = sd.detect(c)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)

		# show the output image
		cv2.imshow("Image", image)
		#cv2.waitKey(0)
	# show the frame
	#cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()
