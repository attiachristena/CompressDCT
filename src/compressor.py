import numpy as np
import scipy.fft as scipy_fft
from PIL import Image

def compress_image(img_matrix, F, d):
    """ Compresses an image using block-wise 2D Discrete Cosine Transform (DCT) and frequency filtering.
    Parameters
    ----------
    img_matrix : numpy.ndarray
        Input image matrix (2D array) with pixel values in the range [0, 255].
    F : int
        Block size for DCT (F x F).
    d : int
        Threshold for frequency filtering.
    Returns
    -------
    cropped_matrix : numpy.ndarray
        Cropped image matrix.
    compressed_matrix : numpy.ndarray
        Compressed image matrix.
    """
    # Obtain the current dimensions of the image matrix
    current_h, current_w = img_matrix.shape

    # Calculate the new dimensons that are multiples of F
    new_h = current_h - (current_h % F)
    new_w = current_w - (current_w % F)

    # Crop the image matrix to the new dimensions
    cropped_matrix = img_matrix[:new_h, :new_w]

    # Initialize the compressed matrix with zeros
    compressed_matrix = np.zeros((new_h, new_w))

   
    for i in range(0, new_h, F):
        for j in range(0, new_w, F):
            # Extract the current block of size F x F
            block = cropped_matrix[i : i + F, j : j + F]
            
            # Apply the 2D Discrete Cosine Transform (dctn) to the block
            dct_block = scipy_fft.dctn(block, norm='ortho')

            # Zero out the coefficients where k + l >= d
            for k in range(F):
                for l in range(F):
                    if k + l >= d:
                        dct_block[k, l] = 0.0

            # Apply the inverse 2D Discrete Cosine Transform (idctn)
            idct_block = scipy_fft.idctn(dct_block, norm='ortho')
            
            # Round to the nearest integer
            round_block = np.round(idct_block)
            
            # Set negative values to zero and values > 255 to 255 
            clipped_block = np.clip(round_block, 0, 255)
            
            # Insert the modified block into the final matrix
            compressed_matrix[i : i + F, j : j + F] = clipped_block

    return cropped_matrix, compressed_matrix.astype(np.uint8)

def plot_results(cropped, compressed):
    """ Plots the original cropped image and the compressed image side by side for comparison.
    Parameters
    ----------
    cropped : numpy.ndarray
        Cropped original image matrix.
    compressed : numpy.ndarray
        Compressed image matrix.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))

    # Display the cropped original image
    plt.subplot(1, 2, 1)
    plt.imshow(cropped, cmap='gray', vmin=0, vmax=255)
    plt.title('Cropped Original Image')
    plt.axis('off')

    # Display the compressed image
    plt.subplot(1, 2, 2)
    plt.imshow(compressed, cmap='gray', vmin=0, vmax=255)
    plt.title('Compressed Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load the image and convert it to grayscale
    img = Image.open('/Users/christenaattia/Desktop/Compress_DCT/images/80x80.bmp').convert('L')
    img_matrix = np.array(img)
    
    # Set block size F and threshold d
    F = 8
    d = 14

    # Compress the image
    cropped, compressed = compress_image(img_matrix, F, d)

    # Plot the results
    plot_results(cropped, compressed)