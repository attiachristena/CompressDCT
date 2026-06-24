# main.py
import tkinter as tk
from src.gui import AppCompressione

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCompressione(root)
    root.mainloop()