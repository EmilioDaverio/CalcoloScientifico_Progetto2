# src/test.py
import numpy as np
import timeit
import utilss
import load_matrix
import generate_graphs

def run_test():
    # Matrice di test 8x8
    test_matrix = np.array([
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]
    ])
    print(test_matrix)

    # Verifica DCT2
    dct2_result =utilss.dct2_created(test_matrix)
    expected_dct2_result = np.array([
        [1.11e+03, 4.40e+01, 7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02],
        [7.71e+01, 1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01],
        [4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01],
        [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02],
        [-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01],
        [-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01],
        [7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01],
        [1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00]
    ])

    print("\n-----------------------TEST DCT2 HomeMade-------------------------")
    print(dct2_result)
    assert np.allclose(dct2_result, expected_dct2_result, rtol=1e-2), "DCT2 HomeMade test failed!"

    # Verifica DCT monodimensionale sulla prima riga
    # Prima riga della matrice di test
    a = test_matrix[0, :]
    dct = utilss.dct_created(a)
    expected_dct = np.array([4.01e+02, 6.60e+00, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01])
    formatted_dct = ["{:.2e}".format(val) for val in dct]
    print("\n-----------------------TEST DCT HomeMade-------------------------")
    print(formatted_dct)
    assert np.allclose(dct, expected_dct, rtol=1e-2), "DCT HomeMade test failed!"

    # Verifica DCT2 con libreria sulla matrice di test
    dct2_result_lib = utilss.dct2_library(test_matrix)
    print("\n-----------------------TEST DCT2 Library-------------------------")
    print(dct2_result_lib)
    assert np.allclose(dct2_result_lib, expected_dct2_result, rtol=1e-2), "DCT2 Library test failed!"

    # Verifica DCT con libreria sulla prima riga
    dct_lib = utilss.dct_library(a)
    formatted_dct_lib = ["{:.2e}".format(val) for val in dct_lib]
    print("\n-----------------------TEST DCT Library-------------------------")
    print(formatted_dct_lib)
    assert np.allclose(dct_lib, expected_dct, rtol=1e-2), "DCT Library test failed!"

def test_N():
    # Testo le prestazioni della DCT2 su matrici di dimensioni crescenti fino a 1024x1024.
    # da 50x50 a 1024x1024, con incrementi di 50.
    matrix_dimensions = list(range(50, 901, 50))

    # Creo una lista vuota per memorizzare i tempi di esecuzione della DCT2 utilizzando la libreria scipy.
    times_scipy_dct = []

    # Creo una lista vuota per memorizzare i tempi di esecuzione della mia implementazione della DCT2.
    times_my_dct = []

    for n in matrix_dimensions:
        print("Dimension: ", n)
        # Imposto un seed per il generatore di numeri casuali per garantire la riproducibilità dei test.
        np.random.seed(5)

        # Genero una matrice NxN con valori casuali compresi tra 0 e 255.
        matrix = np.random.uniform(low=0.0, high=255.0, size=(n, n))

        # Misuro il tempo di esecuzione della DCT2 utilizzando la libreria scipy.
        time_scipy = timeit.timeit(lambda: utilss.dct2_library(matrix), number=1)
        times_scipy_dct.append(time_scipy)

        # Misuro il tempo di esecuzione della mia implementazione della DCT2.
        time_my_dct = timeit.timeit(lambda: utilss.dct2_created(matrix), number=1)
        times_my_dct.append(time_my_dct)

    # Restituisco i tempi di esecuzione e le dimensioni delle matrici testate.
    return times_scipy_dct, times_my_dct, matrix_dimensions

if __name__ == "__main__":
    run_test()
    times_scipy_dct, times_my_dct, matrix_dimensions = test_N()

    # Genero e visualizzo un grafico con i tempi di esecuzione.
    generate_graphs.plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions)