import numpy as np
import timeit
import utils.utils as utils
import load_matrix
import graph_gen

def run_test():
    a = load_matrix.load_matrix()[0, :]  # Carica la prima riga della matrice
    dct = utils.dct_created(a)
    formatted_dct = ["{:.2e}".format(val) for val in dct]
    print("\n-----------------------TEST DCT HomeMade-------------------------")
    print(formatted_dct)

    input_matrix = load_matrix.load_matrix()  # Carica l'intera matrice
    dct2_result = utils.dct2_created(input_matrix)
    print("\n-----------------------TEST DCT2 HomeMade-------------------------")
    print(dct2_result)

    dct = utils.dct_library(a)
    formatted_dct = ["{:.2e}".format(val) for val in dct]
    print("\n-----------------------TEST DCT Library-------------------------")
    print(formatted_dct)

    dct2_result = utils.dct2_library(input_matrix)
    print("\n-----------------------TEST DCT2 Library-------------------------")
    print(dct2_result)

def test_N():
    matrix_dimensions = list(range(50, 951, 50))
    times_scipy_dct = []
    times_my_dct = []

    for n in matrix_dimensions:
        print("Dimension: ", n)
        np.random.seed(5)
        matrix = np.random.uniform(low=0.0, high=255.0, size=(n, n))

        time_scipy = timeit.timeit(lambda: utils.dct2_library(matrix), number=1)
        times_scipy_dct.append(time_scipy)

        time_my_dct = timeit.timeit(lambda: utils.dct2_created(matrix), number=1)
        times_my_dct.append(time_my_dct)

    return times_scipy_dct, times_my_dct, matrix_dimensions

if __name__ == "__main__":
    run_test()
    times_scipy_dct, times_my_dct, matrix_dimensions = test_N()
    graph_gen.plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions)
