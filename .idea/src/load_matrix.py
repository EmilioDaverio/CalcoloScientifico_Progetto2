# src/load_matrix.py
import pandas as pd

# Carichiamo la matrice e la visualizziamo a terminale
def load_matrix(filename='C:\\Users\\Sistema\\Desktop\\Progetto_2\\Parte1\\untitled\\matrix.csv'):
    # Caricamento della matrice dal file CSV
    df = pd.read_csv(filename, header=None)
    matrix_loaded = df.values
    return matrix_loaded

if __name__ == "__main__":
    matrix = load_matrix()
    print("Matrice caricata dal file CSV:")
    print(matrix)