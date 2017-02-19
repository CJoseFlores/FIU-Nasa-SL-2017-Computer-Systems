import argparse
import cv2
import numpy as np

# Create Argument Parser with arguments of an HSV color.
ap = argparse.ArgumentParser(description="Converts a GIMP HSV color to an Open CV HSV color.")
ap.add_argument("Hue", help="Specify the Hue value of the HSV color.",type=int)
ap.add_argument("Saturation",help="Specify the Saturation value of the HSV color.",type=int)
ap.add_argument("Value",help="Specify the Brightness of the HSV color.",type=int)

args = vars(ap.parse_args())

# Convert GIMP HSV to Open CV HSV
cvHue = round((args["Hue"]/360) * 179) # GIMP Hue range is 0-360
cvSat = round((args["Saturation"]/100) * 255) # GIMP Saturation range is 0-100
cvVal = round((args["Value"]/100) * 255) # GIMP Brightness range is 0-100

print("H:"+str(cvHue)+"  S:"+str(cvSat)+"  V:"+str(cvVal))