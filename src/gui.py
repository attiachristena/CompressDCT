import os
import customtkinter as ctk 
from tkinter import filedialog, messagebox

# Importiamo dal nostro file compressor.py
from compressor import import_image, compress_image, plot_results

# Impostazioni globali del tema moderno
ctk.set_appearance_mode("Dark")  # Opzioni: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Tema dei bottoni

class ModernCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurazione finestra principale
        self.title("Ottimizzatore Immagini DCT")
        self.geometry("500x450")
        self.resizable(False, False)

        # Variabile per salvare il percorso del file
        self.file_path = ""

        self._build_ui()

    def _build_ui(self):
        # --- TITOLO ---
        self.title_label = ctk.CTkLabel(self, text="Compressione JPEG", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(self, text="Basato su Trasformata Discreta del Coseno (DCT2)", font=ctk.CTkFont(size=12), text_color="gray")
        self.subtitle_label.pack(pady=(0, 20))

        # --- SEZIONE 1: SELEZIONE FILE ---
        self.frame_file = ctk.CTkFrame(self)
        self.frame_file.pack(pady=10, padx=20, fill="x")

        self.btn_browse = ctk.CTkButton(self.frame_file, text="📁 Sfoglia Immagine", command=self.seleziona_file)
        self.btn_browse.pack(pady=15, padx=15, side="left")

        self.lbl_filename = ctk.CTkLabel(self.frame_file, text="Nessun file selezionato", text_color="gray")
        self.lbl_filename.pack(pady=15, padx=15, side="left", fill="x", expand=True)

        # --- SEZIONE 2: PARAMETRI ---
        self.frame_params = ctk.CTkFrame(self)
        self.frame_params.pack(pady=10, padx=20, fill="x")

        # F Parameter
        self.lbl_f = ctk.CTkLabel(self.frame_params, text="Ampiezza macro-blocco (F):", font=ctk.CTkFont(weight="bold"))
        self.lbl_f.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")
        
        self.entry_f = ctk.CTkEntry(self.frame_params, width=80, justify="center")
        self.entry_f.insert(0, "8") # Valore di default
        self.entry_f.grid(row=0, column=1, padx=20, pady=(15, 10), sticky="e")

        # d Parameter
        self.lbl_d = ctk.CTkLabel(self.frame_params, text="Soglia di taglio frequenze (d):", font=ctk.CTkFont(weight="bold"))
        self.lbl_d.grid(row=1, column=0, padx=20, pady=(10, 15), sticky="w")
        
        self.entry_d = ctk.CTkEntry(self.frame_params, width=80, justify="center")
        self.entry_d.insert(0, "5") # Valore di default
        self.entry_d.grid(row=1, column=1, padx=20, pady=(10, 15), sticky="e")

        # --- SEZIONE 3: PULSANTE DI AVVIO ---
        self.btn_start = ctk.CTkButton(self, text="ELABORA E COMPRIMI", 
                                       font=ctk.CTkFont(size=14, weight="bold"), 
                                       height=45, 
                                       fg_color="#2FA572", hover_color="#1D7850",
                                       command=self.avvia_elaborazione)
        self.btn_start.pack(pady=25, padx=20, fill="x")

    def seleziona_file(self):
        """ Apre la finestra di dialogo per il file e aggiorna la UI """
        path = filedialog.askopenfilename(
            title="Seleziona Immagine",
            filetypes=[("Immagini", "*.bmp *.jpg *.jpeg *.png"), ("Tutti i file", "*.*")]
        )
        if path:
            self.file_path = path
            nome_file = os.path.basename(path)
            self.lbl_filename.configure(text=nome_file, text_color="white")

    def avvia_elaborazione(self):
        """ Raccoglie i dati, controlla gli errori e lancia l'algoritmo """
        if not self.file_path:
            messagebox.showwarning("Attenzione", "Per favore, seleziona un'immagine prima di procedere.")
            return

        try:
            # Recupera i valori in formato intero
            F = int(self.entry_f.get())
            d = int(self.entry_d.get())
        except ValueError:
            messagebox.showerror("Errore di Inserimento", "I valori F e d devono essere numeri interi.")
            return

        # Validazione matematica richiesta dalla traccia
        if F <= 0:
            messagebox.showerror("Errore", "L'ampiezza F deve essere maggiore di 0.")
            return
        
        limite_d = 2 * F - 2
        if d < 0 or d > limite_d:
            messagebox.showerror("Errore", f"Con F={F}, la soglia d deve essere compresa tra 0 e {limite_d}.")
            return

        # Esecuzione
        try:
            # Cambia il testo del bottone durante il caricamento (opzionale ma rende l'app più "viva")
            self.btn_start.configure(text="ELABORAZIONE IN CORSO...", state="disabled")
            self.update()

            img_matrix = import_image(self.file_path)
            cropped, compressed = compress_image(img_matrix, F, d)
            
            self.btn_start.configure(text="ELABORA E COMPRIMI", state="normal")
            
            plot_results(cropped, compressed)

        except Exception as e:
            self.btn_start.configure(text="ELABORA E COMPRIMI", state="normal")
            messagebox.showerror("Errore Critico", f"Si è verificato un errore durante l'elaborazione:\n\n{str(e)}")

if __name__ == "__main__":
    app = ModernCompressorApp()
    app.mainloop()