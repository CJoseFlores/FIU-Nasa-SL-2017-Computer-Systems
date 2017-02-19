import argparse
import cv2
import numpy as np

# Create Argument Parser with arguments of an RGB color.
ap = argparse.ArgumentParser()
ap.add_argument("Red", help="Specify the Red value of the RGB color.")
ap.add_argument("Green",help="Specify the Green value of the RGB color.")
ap.add_argument("Blue",help="Specify the Blue value of the RGB color.")

args = vars(ap.parse_args())

# Convert the specified RGB to HSV needed for python-Open CV
color = np.uint8([[[args["Blue"],args["Green"],args["Red"]]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
print (hsv_color)
