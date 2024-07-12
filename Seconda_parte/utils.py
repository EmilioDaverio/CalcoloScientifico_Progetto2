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
global label_path, entry_variable_f, entry_variable_d, file_path, text_log
file_path = None

class DCTApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Compressione Immagini .bmp in Toni di Grigio")
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
        global label_path, entry_variable_f, entry_variable_d, text_log

        # Frame per la selezione del file
        frame_file = ttk.LabelFrame(self.master, text="Selezione File", padding=10)
        frame_file.pack(pady=10, padx=10, fill="x", expand="yes")

        label_path = tk.Label(frame_file, text="Nessun file selezionato", wraplength=300, font=self.custom_font)
        label_path.pack(pady=5)

        browse_remove_frame = ttk.Frame(frame_file)
        browse_remove_frame.pack(pady=5)

        browse_button = ttk.Button(browse_remove_frame, text="Sfoglia", command=browse_file, style="Material.TButton")
        browse_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(browse_remove_frame, text="Rimuovi Foto Selezionata", command=remove_file, style="Material.TButton")
        remove_button.pack(side=tk.LEFT, padx=5)

        # Frame per i parametri di compressione
        frame_parameters = ttk.LabelFrame(self.master, text="Parametri di Compressione", padding=10)
        frame_parameters.pack(pady=10, padx=10, fill="x", expand="yes")

        label_variable_f = tk.Label(frame_parameters, text="Inserisci la variabile F:", font=self.custom_font)
        label_variable_f.pack(pady=5)

        entry_variable_f = tk.Entry(frame_parameters, font=self.custom_font)
        entry_variable_f.pack(pady=5)

        label_variable_d = tk.Label(frame_parameters, text="Inserisci la variabile d (intero):", font=self.custom_font)
        label_variable_d.pack(pady=5)

        entry_variable_d = tk.Entry(frame_parameters, font=self.custom_font)
        entry_variable_d.pack(pady=5)

        compress_button = ttk.Button(frame_parameters, text="Comprimi", command=flow, style="Material.TButton")
        compress_button.pack(pady=5)

        # Frame per i log
        frame_log = ttk.LabelFrame(self.master, text="Log", padding=10)
        frame_log.pack(pady=10, padx=10, fill="both", expand="yes")

        text_log = tk.Text(frame_log, wrap="word", height=10, font=self.custom_font)
        text_log.pack(pady=5, fill="both", expand="yes")

        reset_log_button = ttk.Button(frame_log, text="Ripulisci Log", command=reset_log, style="Material.TButton")
        reset_log_button.pack(pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.master.destroy()
        self.master.quit()

def create_first_interface():
    global label_path, entry_variable_f, entry_variable_d

    root = tk.Tk()
    app = DCTApp(root)
    root.mainloop()

def flow():
    F, d, image_path = check_variables()
    if F is None or d is None or image_path is None:
        return
    blocks = divide_image_into_blocks(image_path, F)
    blocks_dct_quantized = apply_dct2(blocks, F, d)

    for i, block_dct_quantized in enumerate(blocks_dct_quantized[:3]):
        log(f"Risultati della DCT2 quantizzata per blocco {i + 1}:\n{block_dct_quantized}\n")

    blocks_idct_rounded = apply_idct2(blocks_dct_quantized)
    save_compressed_image(blocks_idct_rounded)

    show_images(Image.open(file_path).convert('L'), Image.open("compressed_image.bmp"))

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Bitmap files", "*.bmp")])
    if file_path:
        label_path.config(text="File selezionato: " + file_path)

        img = Image.open(file_path).convert('L')
        img_width, img_height = img.size
        img.close()

        label_path.config(text=f"File selezionato: {file_path}\n\nDimensioni immagine: {img_width}x{img_height}")
    else:
        label_path.config(text="Nessun file selezionato")

def remove_file():
    global file_path
    file_path = None
    label_path.config(text="Nessun file selezionato")
    log("File selezionato rimosso.")

def reset_log():
    text_log.delete(1.0, tk.END)
    log("Log ripulito.")

def show_images(original_image, compressed_image):
    def on_closing():
        original_image.close()
        compressed_image.close()

        root.destroy()
        root.quit()

    root = tk.Tk()
    root.title("Immagine Originale e Compressa")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.imshow(original_image, cmap="gray", interpolation="nearest")
    ax1.set_title("Immagine Originale")
    ax1.axis("off")

    ax2.imshow(compressed_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
    ax2.set_title("Immagine Compressa")
    ax2.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def check_variables():
    global entry_variable_f, entry_variable_d, file_path

    compressed_image_path = "compressed_image.bmp"

    try:
        if os.path.exists(compressed_image_path):
            os.remove(compressed_image_path)
            log("Rimossa l'immagine compressa esistente.")
    except Exception as e:
        log(f"Errore durante la rimozione dell'immagine compressa: {str(e)}")

    F = entry_variable_f.get()
    d = entry_variable_d.get()

    if not file_path:
        messagebox.showerror("Errore", "Seleziona un'immagine.")
        return None, None, None

    if not F:
        messagebox.showerror("Errore", "Inserisci il valore di F.")
        return None, None, None

    if not d:
        messagebox.showerror("Errore", "Inserisci il valore di d.")
        return None, None, None

    if not is_integer(F):
        messagebox.showerror("Errore", "F deve essere un numero intero")
        return None, None, None

    if not is_integer(d):
        messagebox.showerror("Errore", "d deve essere un numero intero")
        return None, None, None

    F = int(F)
    d = int(d)

    if F < 0:
        messagebox.showerror("Errore", "F deve essere maggiore o uguale a 0")
        return None, None, None
    if d < 0:
        messagebox.showerror("Errore", "d deve essere maggiore o uguale a 0")
        return None, None, None

    try:
        with Image.open(file_path) as img:
            img_width, img_height = img.size

        if F > img_width or F > img_height:
            messagebox.showerror("Errore", "Il valore di F non può superare le dimensioni dell'immagine.")
            return None, None, None

        log(f"Dimensioni immagine selezionata: {img_width}x{img_height}")

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il recupero delle dimensioni dell'immagine: {str(e)}")
        return None, None, None

    if d > 2 * F - 2 or d < 0:
        messagebox.showerror("Errore", "Il valore di d deve essere compreso tra 0 e 2F-2.")
        return None, None, None

    log("Tutti i controlli sono stati superati.")
    return F, d, file_path

def apply_dct2(blocks, F, d):
    blocks_dct_quantized = []
    for block in blocks:
        block_array = np.array(block)
        block_dct = dct(dct(block_array.T, norm='ortho').T, norm='ortho')
        block_dct_quantized = block_dct * (np.abs(np.add.outer(range(F), range(F))) < d)
        blocks_dct_quantized.append(block_dct_quantized)
    return blocks_dct_quantized

def apply_idct2(blocks_dct_quantized):
    blocks_idct_rounded = []
    for block_dct_quantized in blocks_dct_quantized:
        block_idct = idct(idct(block_dct_quantized.T, norm='ortho').T, norm='ortho')
        block_idct_rounded = np.round(block_idct)
        block_idct_rounded[block_idct_rounded < 0] = 0
        block_idct_rounded[block_idct_rounded > 255] = 255
        block_idct_rounded = block_idct_rounded.astype(np.uint8)
        blocks_idct_rounded.append(block_idct_rounded)
    return blocks_idct_rounded

def save_compressed_image(blocks_idct_rounded):
    compressed_image_path = "compressed_image.bmp"
    try:
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

        compressed_image.save(compressed_image_path)
        compressed_image.close()

        log("Immagine compressa salvata con successo.")
    except Exception as e:
        log(f"Errore durante il salvataggio dell'immagine compressa: {str(e)}")

def divide_image_into_blocks(image_path, F):
    blocks = []
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            img_gray = img.convert('L')
            num_blocks_horizontal = img_width // F
            num_blocks_vertical = img_height // F

            for j in range(num_blocks_vertical):
                for i in range(num_blocks_horizontal):
                    x0 = i * F
                    y0 = j * F
                    x1 = x0 + F
                    y1 = y0 + F
                    block = img_gray.crop((x0, y0, x1, y1))
                    blocks.append(block)
    except Exception as e:
        log(f"Errore durante l'elaborazione dell'immagine: {str(e)}")
    return blocks

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def log(message):
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)

def print_blocks(blocks):
    for i, block in enumerate(blocks):
        log(f"Stampa blocco {i + 1}")
        block.show()
