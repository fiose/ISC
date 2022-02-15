import cv2
import sys
import numpy as np
import scipy.io

def load_image_matrix(image_name):
    # open image
    image_path = 'Practical_Tomography/' + image_name + '.png'
    A = cv2.imread(image_path)

    # check if image is square
    (height, width, _) = A.shape
    if not width == height:
        sys.exit(1)

    # transform image into matrix of 0 and 1
    A = A // 255
    A = A[:, :, 0]
    return A

def load_test_matrix():
    n = 4
    random_matrix_array = np.random.uniform(low=0, high=0.5, size=(n, n))
    return random_matrix_array

def main():
    image_name = 'oval'
    matrix = load_image_matrix(image_name)

    image_name = 'test'
    matrix = load_test_matrix()

    # get sums of columns and rows
    colsum = np.sum(matrix, axis=0)  # vertical
    rowsum = np.sum(matrix, axis=1)  # horizontal

    # Save the column and row sums in a file rectangle_HVproj.mat
    # replace 0s with the matching variable
    matlab_result = {"colsum": colsum, "rowsum": rowsum}
    project_file = image_name + '_HVproj' + '.mat'
    scipy.io.savemat(project_file, matlab_result)

if __name__ == "__main__":
    main()

