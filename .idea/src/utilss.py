# utils/utils.py
import numpy as np
import math
from scipy.fft import dct

def create_transformation_matrix(a):
    # Calcolo della lunghezza dell'array
    n = len(a)

    # Creazione del vettore alfa lungo quanto il vettore passato
    alpha = np.zeros(n)

    # Calcolo dei valori in base alla posizione
    alpha[0] = 1 / np.sqrt(n)
    alpha[1:] = np.sqrt(2/n)

    # Creazione della matrice di trasformazione
    transformation_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            transformation_matrix[i, j] = alpha[i] * np.cos((i * math.pi * (2 * j + 1)) / (2 * n))
    return transformation_matrix

# Funzione per DCT creata
def dct_created(input_vector):
    # Creazione della matrice di trasformazione
    transformation_matrix = create_transformation_matrix(input_vector)

    # Calcolo del risultato (c) come la moltiplizazione tra la matrice di trasformazione con il vettore dato in input (f)
    dct_result = np.dot(transformation_matrix, input_vector)
    return dct_result

# Funzione per DCT2 creata
def dct2_created(input_matrix):
    n, m = input_matrix.shape

    # Crezione della matrice
    dct2_result = np.copy(input_matrix.astype('float64'))

    # DCT per ogni colonna
    for j in range(m):
        dct2_result[:, j] = dct_created(dct2_result[:, j])
    # DCT per ogni riga
    for i in range(n):
        dct2_result[i, :] = dct_created(dct2_result[i, :])
    return dct2_result

# Funzione DCT implementata da libreria esterna
def dct_library(f):
    return dct(f, norm='ortho')

# Funzione DCT2 implementata da libreria esterna
def dct2_library(f):
    return dct(dct(f.T, norm='ortho').T, norm='ortho')
