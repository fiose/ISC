"""
Algorithm implementation
"""
import scipy.io
import numpy as np
import cv2


def load_HVproj_file(image_name):
    proj_file = 'Practical_Tomography_Output/' + image_name + '_HVproj' + '.mat'
    matlab_result = scipy.io.loadmat(proj_file)
    return matlab_result

def implementation_with_for_loop(rowsum, colsum, matrix):
    """
    Implemetation using for loops to iterate over rows and columns
    """
    n = len(rowsum)

    # process columns
    for c in range(n):
        Bc = (sum(matrix[:, c]) - colsum[c])/n
        matrix[:, c] = matrix[:, c] - Bc
        for r in range(n):
            if matrix[r, c] < 0.0:
                matrix[r, c] = 0.0
            if matrix[r, c] > 1.0:
                matrix[r, c] = 1.0

    # process rows
    for r in range(n):
        Br = (sum(matrix[r, :]) - rowsum[r])/n
        matrix[r, :] = matrix[r, :] - Br
        for c in range(n):
            if matrix[r, c] < 0.0:
                matrix[r, c] = 0.0
            if matrix[r, c] > 1.0:
                matrix[r, c] = 1.0

    return matrix

def implementation_with_matrix(rowsum, colsum, matrix):
    """
    Implemetation using for matrix operations
    """
    n = len(rowsum)

    # process all columns
    # calculate current colsum
    curr_colsum = np.sum(matrix, axis = 0)
    # create beta column matrix with values to update
    Bc_matrix = np.ones((n, n)) * ((curr_colsum - colsum)/n)
    # update matrix
    matrix = matrix - Bc_matrix
    matrix = matrix.clip(0, 1)

    # process all rows
    # calculate current rowsum
    curr_rowsum = np.sum(matrix, axis = 1)
    # create beta row matrix with values to update
    Br_matrix = np.transpose(np.ones((n, n)) * ((curr_rowsum - rowsum)/n))
    # update matrix
    matrix = matrix - Br_matrix
    matrix = matrix.clip(0, 1)

    return matrix


def reconstruct_image(rowsum, colsum, generate_analysis = False):
    eps = 0.0001
    MAX_ITER = 200
    current_iter = 0
    n = len(rowsum)
    matrix = np.zeros((n, n))
    last_matrix = matrix

    # useful information to analyze result if desired
    analysis = { 'deltas': [], 'matrices': [] }

    while current_iter < MAX_ITER:
        current_iter += 1

        # choose implementation
        #matrix = implementation_with_for_loop(rowsum, colsum, matrix)
        matrix = implementation_with_matrix(rowsum, colsum, matrix)

        # calculate average pixel absolute difference between current matrix and last matrix
        pixel_delta = 1./(n*n) * np.sum(np.abs(matrix - last_matrix))

        if generate_analysis == True:
            analysis['deltas'].append(pixel_delta)
            analysis['matrices'].append(matrix)

        if pixel_delta < eps:
            break
        last_matrix = matrix

    analysis['final_colsum'] = np.sum(matrix, axis = 0)
    analysis['final_rowsum'] = np.sum(matrix, axis = 1)

    return matrix, analysis


def translate_matrix_to_pixels(matrix):
    n = len(matrix[0, :])
    new_matrix = np.zeros((n, n, 3), int)
    for r in range(n):
        for c in range(n):
            value = matrix[r, c]
            if value < 0.5:
                new_matrix[r, c] = [0, 0, 0]
            else:
                new_matrix[r, c] = [255, 255, 255]
    return new_matrix


def save_image(image_name, image_matrix):
    recfile = image_name + '.png'
    cv2.imwrite(recfile, image_matrix)


def main():
    image_name = 'rock'
    # get the colsum and rowsum from the projection file
    projection = load_HVproj_file(image_name)
    colsum = projection["colsum"][0]
    rowsum = projection["rowsum"][0]
    # reconstruct the approximate values of the image matrix
    image_matrix, _ = reconstruct_image(rowsum, colsum)
    # turn the approximate values of the image matrix into pixels
    image_matrix = translate_matrix_to_pixels(image_matrix)
    # save the image matrix to a png file
    save_image('Practical_Tomography_Output/'+image_name+'_reconstructed', image_matrix)


if __name__ == "__main__":
    main()
