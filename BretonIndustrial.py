import sqlite3
import tkinter as tk
import subprocess
import sys
from tkinter import ttk, messagebox, PhotoImage
from datetime import date, timedelta, datetime
from tkinter import simpledialog

#Valores iniciales******************************************************************************************************************************************************************************
conexion = sqlite3.connect('Proyectos/Breton Industrial/Breton industrial.db')  # Cambia el nombre del archivo de la base de datos si es diferente
cursor = conexion.cursor()

#Funciones**************************************************************************************************************************************************************************************
def Operaciones_metalmecanica():
     subprocess.run(['python', 'CapturarOperaciones1.py'])
     
def Ver_horas():
     contrasena = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*')
    # Puedes realizar acciones con la contraseña aquí
     if contrasena == "Produccion1234*":
          #print(f"Contraseña ingresada: {contrasena}")
          subprocess.run(['python', 'VerHoras1.py'])  

def Ver_reporte_tiempo_extra():
     contrasena = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*')
    # Puedes realizar acciones con la contraseña aquí
     if contrasena == "Ingenieria1234*":
          #print(f"Contraseña ingresada: {contrasena}")
          subprocess.run(['python', 'HorasExtra.py'])

def Ver_bonocomida():
     contrasena = simpledialog.askstring("Contraseña", "Ingrese la contraseña:", show='*')
    # Puedes realizar acciones con la contraseña aquí
     if contrasena == "Ingenieria1234*":
          #print(f"Contraseña ingresada: {contrasena}")
          subprocess.run(['python', 'Bonocomida.py'])

def mostrar_datos():
     cursor.execute("SELECT DISTINCT OT, Cliente, Proyecto, FechaInicio, FechaCierre, Estatus FROM 'Proyectos Metalmecanica'")
     resultados = cursor.fetchall()
     # Limpiar el Treeview antes de insertar nuevos datos
     for item in OTs.get_children():
          OTs.delete(item)

     # Insertar los resultados en el Treeview y aplicar etiquetas de color
     for row in resultados:
          OTs.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
          # Aplicar etiquetas de color
          if row[5] == "Cerrado":
               OTs.item(OTs.get_children()[-1], tags=("verde",))

#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton industrial")
ventana.geometry("930x500")  
ventana.resizable(width=False, height=False)
ventana.configure(bg="#000040") 

Logo = PhotoImage(file="Proyectos/Breton Industrial/Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

Imagen_OpMM = tk.PhotoImage(file="Proyectos/Breton Industrial/operaciones.png")
boton_OpMM = tk.Button(ventana, image=Imagen_OpMM, command=Operaciones_metalmecanica, width=75, height=75)
boton_OpMM.place(x=40, y=100)
etiqueta_OpMM = tk.Label(ventana, text="Operaciones\nMetalmecanica", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
etiqueta_OpMM.place(x=25, y=180)

Imagen_revisar_Horas = tk.PhotoImage(file="Proyectos/Breton Industrial/revisarop.png")
boton_revisar_Horas = tk.Button(ventana, image=Imagen_revisar_Horas, command=Ver_horas, width=75, height=75)
boton_revisar_Horas.place(x=150, y=100)
etiqueta_revisar_Horas = tk.Label(ventana, text="Revisar\nHoras", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
etiqueta_revisar_Horas.place(x=135, y=180)

Imagen_ReporteTE = tk.PhotoImage(file="Proyectos/Breton Industrial/tiempoextra.png")
boton_ReporteTE = tk.Button(ventana, image=Imagen_ReporteTE, command=Ver_reporte_tiempo_extra, width=75, height=75)
boton_ReporteTE.place(x=260, y=100)
etiqueta_ReporteTE = tk.Label(ventana, text="Reporte de\ntiempo extra", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
etiqueta_ReporteTE.place(x=245, y=180)

Imagen_BonoComida = tk.PhotoImage(file="Proyectos/Breton Industrial/bonos.png")
boton_BonoComida = tk.Button(ventana, image=Imagen_BonoComida, command=Ver_bonocomida, width=75, height=75)
boton_BonoComida.place(x=370, y=100)
etiqueta_BonoComida = tk.Label(ventana, text="Bono\nde comida", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
etiqueta_BonoComida.place(x=355, y=180)

#Imagen_AgP = tk.PhotoImage(file="agregarproyecto.png")
#boton_AgP = tk.Button(ventana, image=Imagen_AgP, width=75, height=75)
#boton_AgP.place(x=260, y=100)
#etiqueta_AgP = tk.Label(ventana, text="Administracion\nde Proyectos", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_AgP.place(x=245, y=180)

#Imagen_RH = tk.PhotoImage(file="recursoshumanos.png")
#boton_RH = tk.Button(ventana, image=Imagen_RH, width=75, height=75)
#boton_RH.place(x=370, y=100)
#etiqueta_RH = tk.Label(ventana, text="Recursos\nHumanos", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_RH.place(x=355, y=180)

#Imagen_Almacen = tk.PhotoImage(file="almacen.png")
#boton_Almacen = tk.Button(ventana, image=Imagen_Almacen, width=75, height=75)
#boton_Almacen.place(x=480, y=100)
#etiqueta_Almacen = tk.Label(ventana, text="Administracion\nde Materiales", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_Almacen.place(x=465, y=180)

#Imagen_Compras = tk.PhotoImage(file="compras.png")
#boton_Compras = tk.Button(ventana, image=Imagen_Compras, width=75, height=75)
#boton_Compras.place(x=590, y=100)
#etiqueta_Compras = tk.Label(ventana, text="Compras", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_Compras.place(x=575, y=180)

#Imagen_Calidad = tk.PhotoImage(file="calidad.png")
#boton_Calidad = tk.Button(ventana, image=Imagen_Calidad, width=75, height=75)
#boton_Calidad.place(x=700, y=100)
#etiqueta_Calidad = tk.Label(ventana, text="Calidad", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_Calidad.place(x=685, y=180)

#Imagen_Ingenieria = tk.PhotoImage(file="ingenieria.png")
#boton_Ingenieria = tk.Button(ventana, image=Imagen_Ingenieria, width=75, height=75)
#boton_Ingenieria.place(x=810, y=100)
#etiqueta_Calidad = tk.Label(ventana, text="Ingenieria", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=2)
#etiqueta_Calidad.place(x=795, y=180)

estilo_OT = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_OT.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_OT.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
OTs = ttk.Treeview(ventana, columns=(0, 1, 2, 3, 4))
OTs.place(x=60, y=240)
# 5. Agregar encabezados
OTs.heading('#0', text='OT')
OTs.column('#0', width=50, anchor="center")  # Ancho de la Columna 1
OTs.heading('#1', text='Cliente')
OTs.column('#1', width=150, anchor="center")  # Ancho de la Columna 4
OTs.heading('#2', text='Proyecto')
OTs.column('#2', width=200, anchor="center")
OTs.heading('#3', text='Fecha de inicio')
OTs.column('#3', width=150, anchor="center")
OTs.heading('#4', text='Fecha de cierre')
OTs.column('#4', width=150, anchor="center")
OTs.heading('#5', text='Estatus')
OTs.column('#5', width=100, anchor="center")
OTs.tag_configure("verde", background="green")

#Inicio*****************************************************************************************************************************************************************************************
mostrar_datos()

ventana.mainloop()

