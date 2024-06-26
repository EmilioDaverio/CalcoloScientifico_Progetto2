import test
import generate_graphs

print("Esecuzione TEST per DCT e DCT2")
test.run_test()

# Testiamo con valori di N crescenti le performance di DCT home made e la DCT di Scipy
times_scipy_dct, times_my_dct, matrix_dimensions = test.test_N()
generate_graphs.plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions)