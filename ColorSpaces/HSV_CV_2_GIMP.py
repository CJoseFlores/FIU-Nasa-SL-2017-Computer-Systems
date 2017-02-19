import argparse
import cv2
import numpy as np

# Create Argument Parser with arguments of an HSV color.
ap = argparse.ArgumentParser(description="Converts an Open CV HSV color to a GIMP HSV color.")
ap.add_argument("Hue", help="Specify the Hue value of the HSV color.",type=int)
ap.add_argument("Saturation",help="Specify the Saturation value of the HSV color.",type=int)
ap.add_argument("Value",help="Specify the Brightness of the HSV color.",type=int)

args = vars(ap.parse_args())

# Convert Open CV HSV to GIMP HSV.
gimpHue = round((args["Hue"]/179) * 360) # CV Hue range is from 0-179
gimpSat = round((args["Saturation"]/255) * 100) # CV Saturation range is from 0-255
gimpVal = round((args["Value"]/255) * 100) # CV Value range is from 0-255

print("H:"+str(gimpHue)+"  S:"+str(gimpSat)+"  V:"+str(gimpVal))