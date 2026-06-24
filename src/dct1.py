import numpy as np

def compute_D(N):
    """
    It constructs the orthonormal DCT matrix of size N x N.

    Every row of the matrix represents a basis function 
    of the discrete cosine transform.

    Parameters
    ----------
    N : int
        Dimensions of the matrix.

    Returns
    -------
    numpy.ndarray
        Orthonormal DCT matrix of size N x N.
    """

    D = np.zeros((N, N))

    # Fattori di normalizzazione
    alpha = np.full(N, np.sqrt(2 / N))
    alpha[0] = 1 / np.sqrt(N)

    for k in range(N):
        for i in range(N):
            D[k, i] = alpha[k] * np.cos((k * np.pi * (2 * i + 1)) / (2 * N))

    return D


def myDCT_1D(f, D=None):
    """
    Calculates the 1D Discrete Cosine Transform (DCT) of a vector.

    Parameters
    ----------
    f : numpy.ndarray
        Vector of samples in the spatial domain.
    D : numpy.ndarray, optional
        Orthonormal DCT matrix of size N x N.
        If not provided, it will be computed automatically.

    Returns
    -------
    numpy.ndarray
        Vector of DCT coefficients.
    """

    if D is None:
        D = compute_D(len(f))

    return D @ f


def myIDCT_1D(c, D=None):
    """
    Calculates the 1D Inverse Discrete Cosine Transform (IDCT) of a vector.

    Since the matrix D is orthonormal, the inverse transform
    coincides with the product by the transpose.

    Parameters
    ----------
    c : numpy.ndarray
        Vector of DCT coefficients.
    D : numpy.ndarray, optional
        Orthonormal DCT matrix of size N x N.
        If not provided, it will be computed automatically.

    Returns
    -------
    numpy.ndarray
        Vector reconstructed in the spatial domain.
    """

    if D is None:
        D = compute_D(len(c))

    return D.T @ c
