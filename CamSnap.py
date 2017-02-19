import argparse
import time
import cv2
import imutils

# Create an Argument Parser and make a File Name Argument.
ap = argparse.ArgumentParser()
ap.add_argument("File Name", help="Enter the desired file name, no file extension.")

# Pass parser to a dictionary.
args = vars(ap.parse_args())

# Link camera stream.
camera = cv2.VideoCapture(0)

# Allow the camera to warmup.
time.sleep(2)

# Grab a few frames to ensure clarity.
for x in range (0, 5):
    ret, image = camera.read()
    resized = imutils.resize(image, width=300)
    ration = image.shape[0] / float(resized.shape[0])

# Write the frame to a file.
cv2.imwrite("images/"+args["File Name"]+".png", image)

camera.release()