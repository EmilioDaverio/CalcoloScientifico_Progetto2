import matplotlib.pyplot as plt
import numpy as np

def plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions):
    # Calcolo delle curve di riferimento per n^3 e n^2 * log(n)
    # Dividiamo per 10^6 e 10^8 rispettivamente per scalare i valori in modo che siano comparabili con i tempi di esecuzione
    n3 = [n**3 /1e5 for n in matrix_dimensions]
    n2_logn = [n**2 * np.log(n) / 1e8 for n in matrix_dimensions]

    # Creazione della figura del grafico con dimensioni 10x6 pollici
    plt.figure(figsize=(10, 6))

    # Aggiunta della curva dei tempi di esecuzione della DCT2 utilizzando la libreria scipy
    plt.semilogy(matrix_dimensions, times_scipy_dct, label='Library DCT2', color="tab:green")
    # Aggiunta della curva di riferimento n^2 * log(n)
    plt.semilogy(matrix_dimensions, n2_logn, label='n^2 * log(n)', color="tab:green", linestyle='dashed')

    # Aggiunta della curva dei tempi di esecuzione della tua implementazione della DCT2
    plt.semilogy(matrix_dimensions, times_my_dct, label='DCT2 created', color="tab:blue")
    # Aggiunta della curva di riferimento n^3
    plt.semilogy(matrix_dimensions, n3, label='n^3', color="tab:blue", linestyle='dashed')

    # Impostazione delle etichette degli assi e del titolo del grafico
    plt.xlabel('Dimensione N')
    plt.ylabel('Tempo di esecuzione in secondi')
    plt.title('Tempi di esecuzione della DCT2 al variare della dimensione N')

    # Aggiunta della legenda per identificare le diverse curve
    plt.legend()

    # Aggiunta di una griglia al grafico
    plt.grid(True)

    # Salvataggio dell'immagine del grafico in un file PNG
    #plt.savefig('Parte1/untiled/grafico_dct_times.png')

    # Visualizzazione del grafico
    plt.show()