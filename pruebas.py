import tkinter as tk
from tkinter import simpledialog

def solicitar_contrasena():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    # Solicitar la contraseña usando un cuadro de diálogo simple
    contrasena = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*')

    # Puedes realizar acciones con la contraseña aquí
    if contrasena:
        print(f"Contraseña ingresada: {contrasena}")
    else:
        print("No se ingresó ninguna contraseña.")

# Llama a la función para probarla
solicitar_contrasena()
