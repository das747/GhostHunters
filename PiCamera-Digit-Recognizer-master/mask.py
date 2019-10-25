import cv2
import numpy as np

# while(1):


image = cv2.imread('1.JPG')

# _, image = cap.read()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of white color in HSV
# change it according to your need !
lower_white = np.array([0,0,0], dtype=np.uint8)
upper_white = np.array([255,20,255], dtype=np.uint8)

# Threshold the HSV image to get only white colors
mask = cv2.inRange(hsv, lower_white, upper_white)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(image,image, mask= mask)


cv2.imwrite('filtering/hsv.jpg', res)
cv2.imwrite('filtering/mask.jpg', res)
cv2.imwrite('filtering/res.jpg', res)

cv2.destroyAllWindows()