# in this notebook we compare timing serial matrix inversion vs CUDA CPU/GPU matric inversion


import numpy as np
import random
import matplotlib.pyplot as plt
import time
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

def generate_symmetric_matrix_with_zeros(n:int, zero_percentage:float, min_val=1, max_val=10):
    if zero_percentage < 0.01 or zero_percentage > .99:
        raise Exception("zero_percentage should be between 0.01 and 0.99")
    """
    Generate an n x n symmetric matrix with random integers, where
    a certain percentage of entries are zero and symmetric.
    
    Args:
        n (int): Side length of the matrix.
        zero_percentage (float): Value between 0 and 1, e.g., 0.6 for 60% zeros.
        min_val (int): Minimum random integer value.
        max_val (int): Maximum random integer value.
        
    Returns:
        np.ndarray: Symmetric matrix with specified proportion of zeros.
    """
    # Start with a random matrix
    matrix = np.random.randint(min_val, max_val + 1, size=(n, n))
    
    # Make it symmetric
    matrix = (matrix + matrix.T) // 2

    # Total number of unique symmetric positions (excluding diagonal if needed)
    total_entries = n * n
    num_zeros = np.floor(zero_percentage * total_entries)

    # To maintain symmetry, work only on the upper triangle (excluding diagonal)
    zero_positions = set()
    while len(zero_positions) < num_zeros // 2:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        if i != j and (i, j) not in zero_positions and (j, i) not in zero_positions:
            zero_positions.add((i, j))

    # Apply symmetric zeros
    for i, j in zero_positions:
        matrix[i][j] = 0
        matrix[j][i] = 0


    return np.array(matrix)

def loop(n_values, zero_percentages, isDense = True):

    # Initialize time matrix
    times = np.zeros((len(zero_percentages), len(n_values)))

    # Benchmark loop
    for i, zp in enumerate(zero_percentages):
        print(i)
        for j, n in enumerate(n_values):
            matrix = generate_symmetric_matrix_with_zeros(n, zp)

            if isDense:
                start = time.time()
                _ = np.linalg.eigh(matrix)  # more efficient for symmetric matrices
                end = time.time()
            else:
                sparse_mat = csr_matrix(matrix)
                k = len(matrix)-1
                start = time.time()
                sparse_mat = csr_matrix(sparse_mat.astype(float))
                _ = eigsh(sparse_mat, k=k) # more efficient for symmetric matrices
                end = time.time()

            times[i, j] = end - start
    return times 

def main():
    # Parameters
    n_values = range(10, 110, 1)  # from 10 to 200 in steps of 20
    zero_percentages = np.linspace(0, 0.9, 20)  # 0% to 90% zeros

    times = np.zeros((len(zero_percentages), len(n_values)))
    for i in range(10):
        print("new mat")
        times += .1*loop(n_values, zero_percentages)


    # Plot heatmap
    plt.figure(figsize=(10, 6))
    plt.imshow(times, aspect='auto', origin='lower', 
            extent=[min(n_values), max(n_values), min(zero_percentages), max(zero_percentages)])
    plt.colorbar(label='Time to Diagonalize (s)')
    plt.xlabel('Matrix Size (n)')
    plt.ylabel('Zero Percentage')
    plt.title('Diagonalization Time Heatmap')
    plt.tight_layout()
    plt.show()