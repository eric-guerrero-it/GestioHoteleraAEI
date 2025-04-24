"""
Fitxer: manteniment.py

Gestió de les operacions bàsiques de funcionament de l’hotel com el check-in, check-out i reserves.
Inclou control de disponibilitat d’habitacions.
"""
import tkinter as tk

def obrir_finestra_manteniment():
    """
    Obre la finestra principal de manteniment (encara buida).
    """
    root = tk.Tk()
    root.title("Gestió de Manteniment")
    root.geometry("400x300")

    tk.Label(root, text="Mòdul de Manteniment", font=("Arial", 14)).pack(pady=20)

    root.mainloop()
