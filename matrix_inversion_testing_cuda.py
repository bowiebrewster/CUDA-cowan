import numpy as np
import random
import matplotlib.pyplot as plt
import time
import cupy as cp
import importlib
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

import matrix_inversion_testing 
importlib.reload(matrix_inversion_testing)

mat = matrix_inversion_testing.generate_symmetric_matrix_with_zeros


def diagonalize_matrices(matrices, backend='cpu'):
    """
    Diagonalize a list of symmetric matrices using either CPU or GPU.

    Args:
        matrices (list of np.ndarray): List of symmetric matrices.
        backend (str): 'cpu' or 'gpu'.

    Returns:
        list of (eigvals, eigvecs): For each matrix.
    """
    results = []

    if backend == 'cpu':
        for mat in matrices:
            eigvals, eigvecs = np.linalg.eigh(mat)
            results.append((eigvals, eigvecs))

    elif backend == 'gpu':
        
        for mat in matrices:
            mat_gpu = cp.asarray(mat, dtype=cp.float64)
            eigvals, eigvecs = cp.linalg.eigh(mat_gpu)
            results.append((eigvals.get(), eigvecs.get()))  # .get() brings data back to CPU

    else:
        raise ValueError("backend must be 'cpu' or 'gpu'")

    return results

def main(n, zero_percentage, k):
    
    lis = []
    for i in range(k):
        print(i)
        lis.append(mat(n,zero_percentage))
    print(lis)
    #diagonalize_matrices(np.array[lis]) 
    
print(mat(10,.8))
main(10, 80, 10)
