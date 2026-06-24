import numpy as np
from .dct1 import myDCT_1D, myIDCT_1D, compute_D
from scipy.fft import dctn

def myDCT_2D(f):
    """ Calculates the 2D Discrete Cosine Transform (DCT) of a matrix f using the 1D DCT function. 
    Parameters
    ----------
    f : numpy.ndarray
        Input matrix in the spatial domain.
    Returns
    -------
    numpy.ndarray
        Matrix of DCT coefficients.
    """

    c = f.copy()
    N = f.shape[0]

    D = compute_D(N)

    for j in range (N):
        c[:, j] = myDCT_1D(c[:, j], D)
    
    for i in range (N):
        c[i, :] = myDCT_1D(c[i, :], D)

    return c

def myIDCT_2D(c):
    """ Calculates the 2D Inverse Discrete Cosine Transform (IDCT) of a matrix c using the 1D IDCT function.
    Parameters
    ----------
    c : numpy.ndarray
        Input matrix in the frequency domain.
    Returns
    -------
    numpy.ndarray
        Matrix of IDCT coefficients.
    """

    f = c.copy()
    N = c.shape[0]

    D = compute_D(N)

    for j in range (N):
        f[:, j] = myIDCT_1D(f[:, j], D)

    for i in range (N):
        f[i, :] = myIDCT_1D(f[i, :], D)

    return f


def library_dct(f):
    """ Calculates the2D Discrete Cosine Transform (DCT) of a matrix f using the scipy library.
    Parameters
    ----------
    f : numpy.ndarray
        Input matrix in the spatial domain.
    Returns
    -------
    numpy.ndarray
        Matrix of DCT coefficients.
    """
    return dctn(f, norm="ortho")