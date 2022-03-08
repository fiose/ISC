"""
analyze.py is used to test part_one.py and part_two.py together and analyze the algorithm output.
It output information about the how fast the delta decreased (delta.png), how many iterations were necessary,
and comparison between the expected and final colsum/rowsum.
It also outputs the difference between the reconstructed image and the reference image (difference.png), and create
one image for each iteration to help analyze the convergence (k<iteration>_d<delta>.png).
"""
import part_one
import part_two
import matplotlib.pyplot as plt
from pathlib import Path
import os

def main():
    image_names = [ 'oval', 'rectangle', 'rock' ]

    for image_name in image_names:
        print(f'Generating analysis for \'{image_name}\':')
        Path('analyze/' + image_name).mkdir(parents=True, exist_ok=True)

        # get expected matrix
        expected_matrix = part_one.load_image_matrix(image_name)

        # get the colsum and rowsum from the projection file
        projection = part_two.load_HVproj_file(image_name)
        colsum = projection["colsum"][0]
        rowsum = projection["rowsum"][0]

        # reconstruct the approximate values of the image matrix
        # the analysis has information about the image in each iteration and the delta
        _, analysis = part_two.reconstruct_image(rowsum, colsum, True)

        # compare sums
        print('    Sums:')
        print(f'     - col:\n       - expected: {colsum[:10]}\n       - final:    {analysis["final_colsum"][:10]}')
        print(f'     - row:\n       - expected: {rowsum[:10]}\n       - final:    {analysis["final_rowsum"][:10]}')

        # generate delta plot
        print('    Delta: ' + str(analysis['deltas'][-1]))
        plt.figure()
        plt.plot(range(len(analysis['deltas'])), analysis['deltas'])
        plt.xlabel('Iteration')
        plt.ylabel('Delta (log)')
        plt.yscale('log')
        plt.title('Iteration x Delta (log)')
        plt.savefig('analyze/'+image_name+'/delta.png', dpi=300, bbox_inches='tight')

        # generate difference image
        difference = analysis['matrices'][-1] - expected_matrix
        plt.figure()
        plt.matshow(difference)
        plt.savefig('analyze/'+image_name+'/difference.png', dpi=300, bbox_inches='tight')

        # generate iteration images
        print('    Number iterations: ' + str(len(analysis['deltas'])))
        for i, matrix in enumerate(analysis['matrices']):
            # turn the approximate values of the image matrix into pixels
            matrix = part_two.translate_matrix_to_pixels(matrix)
            # save the image matrix to a png file
            part_two.save_image('analyze/'+image_name+'/k'+str(i).zfill(4)+'_d'+str(analysis['deltas'][i]), matrix)

        print('\n')

    print('All images were generated, please check the \'analyze/\' folder')

if __name__ == "__main__":
    main()
