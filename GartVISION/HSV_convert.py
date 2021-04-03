import numpy as np
import cv2

yellow = np.uint8([[[25, 92, 102]]]) #here insert the bgr values which you want to convert to hsv
hsvYellow = cv2.cvtColor(yellow, cv2.COLOR_BGR2HSV)
print(hsvYellow)

lowerLimit = hsvYellow[0][0][0] - 10, 100, 100
upperLimit = hsvYellow[0][0][0] + 10, 255, 255

print(upperLimit)
print(lowerLimit)