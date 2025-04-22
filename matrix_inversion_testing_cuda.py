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
            

    elif backend == 'gpu':
        
        for mat in matrices:
            mat_gpu = cp.asarray(mat, dtype=cp.float64)
            eigvals, eigvecs = cp.linalg.eigh(mat_gpu)
            a = (eigvals.get(), eigvecs.get()) # .get() brings data back to CPU

    else:
        raise ValueError("backend must be 'cpu' or 'gpu'")

    return results

def loop(n, zero_percentage, k, isDense = True):
    
    lis = []
    for i in range(k):
        lis.append(mat(n,zero_percentage))

    if isDense:
        return np.array(lis)
    else:
        matrix = np.array(lis)
        sparse_mat = csr_matrix(matrix)
        k = len(matrix)-1
        sparse_mat = csr_matrix(sparse_mat.astype(float)) 
        return sparse_mat   
    


def benchmark_heatmap(n_values, zero_percentages, k=5, backend='cpu', isDense=True):
    times = np.zeros((len(zero_percentages), len(n_values)))

    for i, zp in enumerate(zero_percentages):
        for j, n in enumerate(n_values):
            print(f"Benchmarking n={n}, zero%={zp*100:.0f}%, backend={backend}")
            
            # Generate matrices
            mats = loop(n, zp, k, isDense=isDense)

            # Time the diagonalization
            start = time.time()
            diagonalize_matrices(mats, backend=backend)
            end = time.time()

            # Store average time per matrix
            times[i, j] = (end - start) / k

    return times


def plot_heatmap(times, n_values, zero_percentages, backend_label="CPU"):
    plt.figure(figsize=(10, 6))
    plt.imshow(times, aspect='auto', origin='lower',
               extent=[min(n_values), max(n_values),
                       min(zero_percentages), max(zero_percentages)])
    plt.colorbar(label='Avg Diagonalization Time (s)')
    plt.xlabel('Matrix Size (n)')
    plt.ylabel('Zero Percentage')
    plt.title(f'Diagonalization Time Heatmap ({backend_label})')
    plt.tight_layout()
    plt.show()
