import cv2
import sys

image_name = 'oval'
image_path = 'Practical_Tomography/' + image_name + '.png'
A = cv2.imread(image_path)

# check if image is square
(width, height, _) = A.shape
if not width == height:
    sys.exit(1)
