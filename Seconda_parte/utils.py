import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkFont
from tkinter import ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageOps
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Dichiarazione delle variabili globali
global label_path, entry_variable_f, entry_variable_d, file_path
file_path = None

class DCTApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Seleziona file .bmp in toni di grigio")
        self.style = ThemedStyle(self.master)
        self.style.set_theme("plastik")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = int(screen_width / 1.5)
        window_height = int(screen_height / 1.5)
        self.master.geometry(f"{window_width}x{window_height}")

        font_size = int(window_height / 45)
        self.custom_font = tkFont.Font(size=font_size)

        self.create_widgets()

    def create_widgets(self):
        global label_path, entry_variable_f, entry_variable_d

        label_path = tk.Label(self.master, text="Nessun file selezionato", wraplength=300, font=self.custom_font)
        label_path.pack(pady=10)

        style = ttk.Style()
        style.configure("Material.TButton", font=self.custom_font)
        browse_button = ttk.Button(self.master, text="Sfoglia", command=browse_file, style="Material.TButton")
        browse_button.pack(pady=5)

        label_variable_f = tk.Label(self.master, text="Inserisci la variabile F:", font=self.custom_font)
        label_variable_f.pack(pady=10)

        entry_variable_f = tk.Entry(self.master, font=self.custom_font)
        entry_variable_f.pack(pady=5)

        label_variable_d = tk.Label(self.master, text="Inserisci la variabile d (intero):", font=self.custom_font)
        label_variable_d.pack(pady=10)

        entry_variable_d = tk.Entry(self.master, font=self.custom_font)
        entry_variable_d.pack(pady=5)

        compress_button = ttk.Button(self.master, text="Compress", command=flow, style="Material.TButton")
        compress_button.pack(pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.master.destroy()  # Chiudi la finestra principale
        self.master.quit()  # Interrompi il ciclo principale di Tkinter

def create_first_interface():
    global label_path, entry_variable_f, entry_variable_d

    root = tk.Tk()
    app = DCTApp(root)
    root.mainloop()

def flow():
    F, d, image_path = check_variables()
    blocks = divide_image_into_blocks(image_path, F)
    blocks_dct_quantized = apply_dct2(blocks, F, d)

    for i, block_dct_quantized in enumerate(blocks_dct_quantized[:3]):
        print(f"Risultati della DCT2 quantizzata per blocco {i + 1}:\n{block_dct_quantized}\n")

    blocks_idct_rounded = apply_idct2(blocks_dct_quantized)
    save_compressed_image(blocks_idct_rounded)

    # Visualizza le immagini originale e compressa
    show_images(Image.open(file_path).convert('L'), Image.open("compressed_image.bmp"))

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])
    if file_path:
        label_path.config(text="File selezionato: " + file_path)

        # Carichiamo l'immagine, la convertiamo in scala di grigi e calcoliamo le dimensioni
        img = Image.open(file_path).convert('L')
        img_width, img_height = img.size
        img.close()

        # Aggiorna la label con il testo che include il percorso dell'immagine e le dimensioni
        label_path.config(text=f"File selezionato: {file_path}\n\nDimensioni immagine: {img_width}x{img_height}")
    else:
        label_path.config(text="Nessun file selezionato")

def show_images(original_image, compressed_image):
    def on_closing():
        print("on closing...")
        original_image.close()
        compressed_image.close()

        root.destroy()  # Chiudi la finestra principale
        root.quit()  # Interrompi il ciclo principale di Tkinter

    root = tk.Tk()
    root.title("Immagine originale e compressa")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Immagine originale
    ax1.imshow(original_image, cmap="gray", interpolation="nearest")
    ax1.set_title("Immagine Originale")
    ax1.axis("off")

    # Immagine compressa
    ax2.imshow(compressed_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
    ax2.set_title("Immagine Compressa")
    ax2.axis("off")

    # Crea la figura in un oggetto FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Imposta l'azione di chiusura sulla finestra principale
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def check_variables():
    global entry_variable_f, entry_variable_d, file_path

    compressed_image_path = "compressed_image.bmp"

    try:
        # Verifica se esiste già un file "compressed_image.bmp"
        if os.path.exists(compressed_image_path):
            os.remove(compressed_image_path)  # Rimuovi il file esistente
            print("Rimossa l'immagine")
    except Exception as e:
        print("Errore durante la rimozione dell'immagine compressa:", str(e))

    # Recupera i valori di F e d dalla label
    F = entry_variable_f.get()
    d = entry_variable_d.get()

    # Verifica che le label e l'immagine non siano vuote. in caso contrario, viene mostrato un messaggio di errore
    if not file_path:
        messagebox.showerror("Errore", "Seleziona un'immagine.")
        return

    if not F:
        messagebox.showerror("Errore", "Inserisci il valore di F.")
        return

    if not d:
        messagebox.showerror("Errore", "Inserisci il valore di d.")
        return

    if not is_integer(F):
        messagebox.showerror("Errore", "F deve essere un numero intero")
        return

    if not is_integer(d):
        messagebox.showerror("Errore", "d deve essere un numero intero")
        return

    F = int(F)
    d = int(d)

    if F < 0:
        messagebox.showerror("Errore", "F deve essere maggiore o uguale a 0")
        return
    if d < 0:
        messagebox.showerror("Errore", "d deve essere maggiore o uguale a 0")
        return

    # Verifichiamo ora che il valore di F non sia superiore all'altezza/larghezza dell'immagine
    try:
        with Image.open(file_path) as img:
            img_width, img_height = img.size

        if F > img_width or F > img_height:
            messagebox.showerror("Errore", "Il valore di F non può superare le dimensioni dell'immagine.")
            return

        # Stampa debug delle dimensioni dell'immagine selezionata
        print("Image Width:", img_width)
        print("Image Height:", img_height)

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il recupero delle dimensioni dell'immagine: {str(e)}")
        return

    # verifichiamo che il valore di d sia compreso tra 0 e 2F-2
    if d > 2 * F - 2 or d < 0:
        messagebox.showerror("Errore", "Il valore di d deve essere compreso tra 0 e 2F-2.")
        return

    # If all checks pass, proceed with compression
    print("All test are ok.")

    return F, d, file_path

def apply_dct2(blocks, F, d):
    # Lista per salvare i blocchi DCT2 quantizzati
    blocks_dct_quantized = []

    # Iteriamo su tutti i blocchi e applichiamo la DCT2
    for block in blocks:
        # Convertiamo il blocco in un array NumPy
        block_array = np.array(block)

        # Applichiamo la DCT2 al blocco usando scipy
        block_dct = dct(dct(block_array.T, norm='ortho').T, norm='ortho')

        # Quantizzazione: Eliminiamo le frequenze con indice di riga + indice di colonna >= d
        block_dct_quantized = block_dct * (np.abs(np.add.outer(range(F), range(F))) < d)

        # Aggiungiamo il blocco DCT2 quantizzato alla lista
        blocks_dct_quantized.append(block_dct_quantized)

    return blocks_dct_quantized

def apply_idct2(blocks_dct_quantized):
    # Lista per salvare i blocchi IDCT2 quantizzati e arrotondati
    blocks_idct_rounded = []

    # Iteriamo su tutti i blocchi quantizzati e applichiamo la IDCT2
    for block_dct_quantized in blocks_dct_quantized:
        # Applichiamo la IDCT2 al blocco usando scipy
        block_idct = idct(idct(block_dct_quantized.T, norm='ortho').T, norm='ortho')

        # Arrotondiamo i valori della matrice IDCT2 al valore intero più vicino
        block_idct_rounded = np.round(block_idct)

        # Impostiamo a 0 i valori negativi
        block_idct_rounded[block_idct_rounded < 0] = 0

        # Impostiamo a 255 i valori maggiori di 255
        block_idct_rounded[block_idct_rounded > 255] = 255

        # Convertiamo la matrice risultante in un array di interi non segnati a 1 byte
        block_idct_rounded = block_idct_rounded.astype(np.uint8)

        # Aggiungiamo il blocco IDCT2 arrotondato e quantizzato alla lista
        blocks_idct_rounded.append(block_idct_rounded)

    return blocks_idct_rounded

def save_compressed_image(blocks_idct_rounded):
    compressed_image_path = "compressed_image.bmp"
    compressed_image = None

    # Verifica se esiste già un file "compressed_image.bmp"
    if os.path.exists(compressed_image_path):
        os.remove(compressed_image_path)  # Rimuovi il file esistente
        print("Rimossa l'immagine")

    try:
        # Ricomponi l'immagine compressa utilizzando i blocchi compressi
        img_width, img_height = Image.open(file_path).size
        compressed_image = Image.new('L', (img_width, img_height))

        F = entry_variable_f.get()
        num_blocks_horizontal = img_width // int(F)

        for j in range(img_height // int(F)):
            for i in range(num_blocks_horizontal):
                x0 = i * int(F)
                y0 = j * int(F)

                block = blocks_idct_rounded.pop(0)

                compressed_image.paste(Image.fromarray(block), (x0, y0))

        # Salva l'immagine compressa nel formato .bmp
        compressed_image.save(compressed_image_path)
        compressed_image.close()

        print("Immagine compressa salvata con successo.")
    except Exception as e:
        print("Errore durante il salvataggio dell'immagine compressa:", str(e))

def divide_image_into_blocks(image_path, F):
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size

            # Converti l'immagine in scala di grigi
            img_gray = img.convert('L')

            # Calcoliamo il numero di blocchi in orizzontale e verticale
            num_blocks_horizontal = img_width // F
            num_blocks_vertical = img_height // F

            blocks = []

            # Iteriamo su tutti i blocchi
            for j in range(num_blocks_vertical):
                for i in range(num_blocks_horizontal):
                    # Calcoliamo le coordinate iniziali e finali del blocco corrente
                    x0 = i * F
                    y0 = j * F
                    x1 = x0 + F
                    y1 = y0 + F

                    # Estraiamo il blocco corrente dall'immagine
                    block = img_gray.crop((x0, y0, x1, y1))
                    blocks.append(block)
            return blocks

    except Exception as e:
        print("Errore durante l'elaborazione dell'immagine:", str(e))
        return blocks

# per verificare se i valori F e d sono interi
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def print_blocks(blocks):
    for i, block in enumerate(blocks):
        print(f"Stampa blocco {i + 1}")
        block.show()
