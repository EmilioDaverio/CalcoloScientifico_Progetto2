# src/generate_matrix.py
import numpy as np
import pandas as pd

def generate_and_save_matrix(filename='matrix.csv'):
    # Generazione della matrice 8x8
    matrix = np.array([
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]
    ])

    # Salvataggio della matrice in un file CSV
    df = pd.DataFrame(matrix)
    df.to_csv(filename, index=False, header=False)

if __name__ == "__main__":
    generate_and_save_matrix()
