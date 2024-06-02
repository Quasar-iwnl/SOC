import numpy as np
from numpy.linalg import eig
import pandas as pd
import matplotlib.pyplot as plt

def PCA(init_array: pd.DataFrame):

    sorted_eigenvalues = None
    sorted_eigenvectors = None
    final_data = None
    dimensions = 2

    # TODO: transform init_array to final_data using PCA
    init_array = (init_array - np.mean(init_array))
    cov = np.cov(init_array)
    eigenvalues, eigenvectors = eig(cov)
    indices = np.argsort(eigenvalues)
    sorted_eigenvalues = eigenvalues[indices]
    sorted_eigenvectors = eigenvectors[indices]
    # END TODO

    return sorted_eigenvalues, final_data


if __name__ == '__main__':
    init_array = pd.read_csv("pca_data.csv", header = None)
    sorted_eigenvalues, final_data = PCA(init_array)
    np.savetxt("transform.csv", final_data, delimiter = ',')
    for eig in sorted_eigenvalues:
        print(eig)

    # TODO: plot and save a scatter plot of final_data to out.png

    # END TODO
