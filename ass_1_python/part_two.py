import scipy.io
import numpy as np
import cv2


def load_HVproj_file(image_name):
    proj_file = image_name + '_HVproj' + '.mat'
    matlab_result = scipy.io.loadmat(proj_file)
    return matlab_result


def reconstruct_image(rowsum, colsum):
    # todo: figure out an appropriate value for eps, 100 is just a random number
    eps = 100
    MAX_ITER = 100
    current_iter = 0
    n = len(rowsum)
    print(f'rowsum: {rowsum}')
    print(f'colsum: {colsum}')
    print(f'n: {n}')
    matrix = np.zeros((n, n))
    print(f'matrix:\n{matrix}')
    while current_iter <= MAX_ITER:
        current_iter += 1
        for c in range(n):
            Bc = (sum(matrix[:, c]) - colsum[c]) / n
            matrix[:, c] = matrix[:, c] - Bc
            # todo: do this min max check without additional for loop. It is required by the assignment
            for r in range(n):
                matrix[r, c] = min(max(matrix[r, c], 0), 1)

        for r in range(n):
            Br = (sum(matrix[r, :]) - rowsum[r])/n
            matrix[r, :] = matrix[r, :] - Br
            # todo: do this min max check without additional for loop. It is required by the assignment
            for c in range(n):
                matrix[r, c] = min(max(matrix[r, c], 0), 1)
        # todo: do this summation without additional for loop. It is required by the assignment
        x = 0
        matrix_init = np.zeros((n, n))
        for r in range(n):
            for c in range(n):
             x += abs((matrix[r, c] - matrix_init[r, c]))
        if (1/(n*n) * x) < eps:
            break
    return matrix


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


def save_image(image_name, image_matrix, k=None, eps=None):
    recfile = image_name + '_HVrec_' + '_k = ' + str(k) + '_eps = ' + str(eps) + '.png'
    cv2.imwrite(recfile, image_matrix)


def main():
    image_name = 'rock'
    # get the colsum and rowsum from the projection file
    projection = load_HVproj_file(image_name)
    colsum = projection["colsum"][0]
    rowsum = projection["rowsum"][0]
    # reconstruct the approximate values of the image matrix
    image_matrix = reconstruct_image(rowsum, colsum)
    # turn the approximate values of the image matrix into pixels
    image_matrix = translate_matrix_to_pixels(image_matrix)
    # save the image matrix to a png file
    save_image(image_name, image_matrix)


if __name__ == "__main__":
    main()
