# import the necessary packages
from picamera.array import PiRGBArray
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
from picamera import PiCamera
import time
import cv2
import imutils
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# initialize the shape detector and color labeler
	sd = ShapeDetector()
	cl = ColorLabeler()

	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		try:
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
		except ZeroDivisionError:
			print "Error. We dont care"
		# detect the shape of the contour and label the color
		shape = sd.detect(c)
		color = cl.label(lab, c)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape and labeled
		# color on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		text = "{} {}".format(color, shape)
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.putText(image, text, (cX, cY),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

		# show the output image
		cv2.imshow("Image", image)
	# show the frame
	#cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
