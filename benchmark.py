import numpy as np
import time
import matplotlib.pyplot as plt

from src.dct2 import myDCT_2D, library_dct

size = [8, 16, 32, 64, 128, 256, 512, 1024]  

def get_random_matrix(N):
    """ Generates a random NxN matrix with values in the range [0, 255].
    Parameters
    ----------
    N : int
        Size of the matrix (N x N).
    Returns
    -------
    numpy.ndarray
        Randomly generated matrix of size N x N.
    """
    return np.random.rand(N, N)

def measure_time(func, matrix, repetitions=10):
    """ Measures the average execution time of a function over a specified number of repetitions.
    Parameters
    ----------
    func : callable
        The function to be measured.
    matrix : numpy.ndarray
        Input matrix to be passed to the function.
    repetitions : int, optional
        Number of times the function will be executed to compute the average time. Default is 10.
    Returns
    -------
    float
        Average execution time in seconds.
    """
    times = []
    for _ in range(repetitions):  
        start = time.perf_counter()
        func(matrix)
        end = time.perf_counter()
        times.append(end - start)
    
    return np.mean(times)  


myDCT_times = []
lib_times = []

for N in size:
    matrix = get_random_matrix(N)

   # Measurement of custom DCT implementation (myDCT_2D)
    myDCT_time = measure_time(myDCT_2D, matrix)
    
    # Measurement of library DCT implementation (scipy.fft.dctn)
    lib_time = measure_time(library_dct, matrix)

    myDCT_times.append(myDCT_time)
    lib_times.append(lib_time)

# Theoretical time complexities for reference
approx_myDCT_time = np.array([float(N)**3 for N in size])
approx_lib_time = np.array([float(N)**2 * np.log(N) for N in size])


if __name__ == "__main__":

    # Print time measurements for each matrix size and corresponding DCT implementations
    for i, N in enumerate(size):
        print(f"Dimensione: {N}x{N} | myDCT_2D: {myDCT_times[i]:.6f}s | Library DCT: {lib_times[i]:.6f}s")

    plt.figure(figsize=(10, 6))
    
    # Plotting the measured times for both implementations
    plt.plot(size, myDCT_times, label='myDCT_2D', marker='o', color='crimson', linewidth=2)
    plt.plot(size, lib_times, label='Library DCT', marker='s', color='royalblue', linewidth=2)
    
    # Plotting the theoretical time complexities for reference
    plt.plot(size, approx_myDCT_time, label='Teorico O(N³)', linestyle='--', color='darkred', alpha=0.7)
    plt.plot(size, approx_lib_time, label='Teorico O(N² log N)', linestyle='--', color='darkblue', alpha=0.7)
    
    plt.xlabel('Dimensione Matrice (N x N)')
    plt.ylabel('Tempo (secondi) [Scala Logaritmica]')
    plt.title('Confronto Performance DCT2: Sperimentale vs Teorico')
    
    # Set y-axis to logarithmic scale for better visualization of time differences
    plt.yscale('log') 
    
    plt.xticks(size, size)  
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    
    # Save the plot and display it
    plt.savefig('benchmark_corretto.png', dpi=300)
    plt.show()


    