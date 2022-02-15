import cv2
import sys
import numpy as np

image_name = 'oval'
image_path = 'Practical_Tomography/' + image_name + '.png'
A = cv2.imread(image_path)

# check if image is square
(width, height, _) = A.shape
if not width == height:
    sys.exit(1)

print(A)
# get sums of columns and rows
# todo: check if vertical and horizontal are correct
colsum = np.sum(A, axis=0)  # vertical
rowsum = np.sum(A, axis=1)  # horizontal
print(colsum)
print(rowsum)


