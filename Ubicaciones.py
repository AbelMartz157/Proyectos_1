import tkinter as tk

def actualizar_interfaz():
    altura = entry_altura.get()
    anchura = entry_anchura.get()

    try:
        altura = int(altura)
        anchura = int(anchura)

        ventana.geometry(f"{anchura}x{altura}")
    except ValueError:
        resultado.config(text="Ingrese valores válidos para altura y anchura", fg="red")

def mostrar_info():
    x, y = ventana.winfo_pointerxy()
    x_rel = x - ventana.winfo_rootx()
    y_rel = y - ventana.winfo_rooty()

    etiqueta_coordenadas.config(text=f"Coordenadas del mouse: X={x_rel}, Y={y_rel}")

    altura = ventana.winfo_height()
    anchura = ventana.winfo_width()
    etiqueta_dimensiones.config(text=f"Dimensiones de la ventana: {anchura}x{altura}")

    ventana.after(100, mostrar_info)  # Actualizar cada 100 milisegundos

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cambiador de Tamaño")

# Crear y colocar los elementos en la ventana
label_altura = tk.Label(ventana, text="Altura:")
label_altura.pack()

entry_altura = tk.Entry(ventana)
entry_altura.pack()

label_anchura = tk.Label(ventana, text="Anchura:")
label_anchura.pack()

entry_anchura = tk.Entry(ventana)
entry_anchura.pack()

boton_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_interfaz)
boton_actualizar.pack()

resultado = tk.Label(ventana, text="")
resultado.pack()

etiqueta_coordenadas = tk.Label(ventana, text="Coordenadas del mouse: X=0, Y=0")
etiqueta_coordenadas.pack()

etiqueta_dimensiones = tk.Label(ventana, text="Dimensiones de la ventana: 0x0")
etiqueta_dimensiones.pack()

# Iniciar el seguimiento de las coordenadas del mouse
ventana.after(100, mostrar_info)

# Configurar evento de cambio de tamaño de la ventana
ventana.bind('<Configure>', mostrar_info)

# Iniciar el bucle de eventos
ventana.mainloop()




