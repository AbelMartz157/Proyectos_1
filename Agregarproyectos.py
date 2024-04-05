import sqlite3
import tkinter as tk
import subprocess
import sys
from tkinter import ttk, messagebox, PhotoImage
from datetime import date, timedelta, datetime
from tkcalendar import DateEntry

#Valores iniciales******************************************************************************************************************************************************************************
conexion = sqlite3.connect('Breton industrial.db')  # Cambia el nombre del archivo de la base de datos si es diferente
cursor = conexion.cursor()
Estatus = ["Abierto", "Cerrado"]
cursor.execute('SELECT DISTINCT OT FROM `Proyectos Metalmecanica`')
ots = cursor.fetchall()
ots = [ot[0] for ot in ots]
#clientes = []
#proyectos = []
cursor.execute('SELECT DISTINCT Cliente FROM `Proyectos Metalmecanica`')
clientes = cursor.fetchall()
clientes = [cliente[0] for cliente in clientes]
cursor.execute('SELECT DISTINCT Proyecto FROM `Proyectos Metalmecanica`')
proyectos = cursor.fetchall()
proyectos = [proyecto[0] for proyecto in proyectos]
NoEnsamble = 0

#Funciones***************************************************************************************************************************************************************************************
def filtro_clientes(event):    
    # Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT Proyecto FROM `Proyectos Metalmecanica` WHERE Cliente = ?", (combo_cliente.get(),))
    proyectos = cursor.fetchall()
    # Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_proyecto['values'] = [proyecto[0] for proyecto in proyectos]

def desbloquear_ensamble(event=None):
     if combo_proyecto.get() != "":
        text_ensamble.configure(state="normal")
        text_budget.configure(state="normal")
        Agregar_ensamble.configure(state="normal")
        Eliminar_ensamble.configure(state="normal")
        date_fechainicio.configure(state="readonly")
        date_fechainicio.set_date(date.today().strftime("%d/%m/%Y"))
        date_fechacierre.configure(state="readonly")
        date_fechacierre.set_date(date.today().strftime("%d/%m/%Y"))
        #Ensambles.configure(state="normal")
     else:
        text_ensamble.configure(state="disabled")
        text_budget.configure(state="disabled")
        Agregar_ensamble.configure(state="disabled")
        Eliminar_ensamble.configure(state="disabled")
        date_fechainicio.configure(state="disabled")
        date_fechacierre.configure(state="disabled")
        #Ensambles.configure(state="disabled")

def agregar_ensambles():
    global NoEnsamble  # Indicar que estás utilizando la variable global
    NoEnsamble += 1    # Modificar la variable global
    try:
        # Intentar convertir el valor a un número flotante
        float(text_budget.get())
        Ensambles.insert("", "end", text= NoEnsamble, values=(text_ensamble.get(), text_budget.get()))
    except ValueError:
        messagebox.showinfo("Industria", "Ingrese un Budget numerico")

def eliminar_ensambles():
    # Obtener el índice de la fila seleccionada
    global NoEnsamble  # Indicar que estás utilizando la variable global
    NoEnsamble = 0
    if Ensambles.selection():
        Ensambles.delete(Ensambles.selection())
        # Recorrer todas las filas del Treeview y actualizar la columna '#0'
        for ensamble in Ensambles.get_children():
            NoEnsamble += 1
            Ensambles.item(ensamble, text=NoEnsamble)
    else:
        messagebox.showinfo("Industria", "Seleccione un ensamble para eliminar")

def desbloquear_botones():
    if text_OT.get():
        Guardar_cambios.configure(state="normal")
        Crear_OT.configure(state="disabled")
    else:
        Guardar_cambios.configure(state="disabled")
        Crear_OT.configure(state="normal")

def nuevo_proyecto():
    if combo_cliente.get() == "":
        messagebox.showinfo("Industria", "Favor de indicar el cliente")
        return
    elif combo_proyecto.get() == "":
        messagebox.showinfo("Industria", "Favor de insertar el nombre del proyecto")
        return
    elif date_fechacierre.get_date() < date_fechainicio.get_date():
        messagebox.showinfo("Industria", "La fecha de cierre es antes que la de inicio")
        return
    
    result = messagebox.askyesno("Confirmación", "¿Deseas generar una Orden de Trabajo para este proyecto?")
    if result:
        # Realizar la consulta para obtener el valor máximo de la columna NoOT
        cursor.execute("SELECT MAX(NoOT) FROM OrdenesTrabajo")
        resultado = cursor.fetchone()
        nueva_OT = int(resultado[0]) + 1 if resultado[0] else 1
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)
        text_OT.insert(0, nueva_OT)
        text_OT.configure(state="disabled")

        datos1 = [(text_OT.get(), combo_cliente.get(), combo_proyecto.get(), date_fechainicio.get_date().strftime("%d/%m/%Y"), date_fechacierre.get_date().strftime("%d/%m/%Y"), "Abierto")]
        # Definir la sentencia SQL para la inserción
        sql1 = '''INSERT INTO OrdenesTrabajo (NoOT, Cliente, Proyecto, FechaInicio, FechaCierre, Estatus)
             VALUES (?, ?, ?, ?, ?, ?)'''
        # Ejecutar la sentencia SQL con la lista de datos
        cursor.executemany(sql1, datos1)
        # Commit para guardar los cambios
        conexion.commit()

        for ensamble in Ensambles.get_children():
            values1 = Ensambles.item(ensamble, 'text')
            values2 = Ensambles.item(ensamble, 'values')
            datos2 = [(text_OT.get(), combo_cliente.get(), combo_proyecto.get(), values1, values2[0], values2[1], date_fechainicio.get_date().strftime("%d/%m/%Y"), date_fechacierre.get_date().strftime("%d/%m/%Y"), "Abierto")]
            # Definir la sentencia SQL para la inserción
            sql2 = '''INSERT INTO 'Proyectos Metalmecanica' (OT, Cliente, Proyecto, NoEnsamble, Ensamble, HorasBudget, FechaInicio, FechaCierre, Estatus)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            # Ejecutar la sentencia SQL con la lista de datos
            cursor.executemany(sql2, datos2)
            # Commit para guardar los cambios
            conexion.commit()

        messagebox.showinfo("Industria", "Datos Guardados con exito")
        desbloquear_botones()

def guardar_cambios():
    result = messagebox.askyesno("Confirmación", "¿Deseas guardar los cambios realizados?")
    if result:
        #Consulta sqlite
        cursor.execute("DELETE FROM OrdenesTrabajo WHERE NoOT= ?", (text_OT.get(),))
        cursor.execute("DELETE FROM 'Proyectos Metalmecanica' WHERE OT= ?", (text_OT.get(),))    
        #Guardar resultados eliminados
        conexion.commit()

        datos1 = [(text_OT.get(), combo_cliente.get(), combo_proyecto.get(), date_fechainicio.get_date().strftime("%d/%m/%Y"), date_fechacierre.get_date().strftime("%d/%m/%Y"), "Abierto")]
        # Definir la sentencia SQL para la inserción
        sql1 = '''INSERT INTO OrdenesTrabajo (NoOT, Cliente, Proyecto, FechaInicio, FechaCierre, Estatus)
             VALUES (?, ?, ?, ?, ?, ?)'''
        # Ejecutar la sentencia SQL con la lista de datos
        cursor.executemany(sql1, datos1)
        # Commit para guardar los cambios
        conexion.commit()

        for ensamble in Ensambles.get_children():
            values1 = Ensambles.item(ensamble, 'text')
            values2 = Ensambles.item(ensamble, 'values')
            datos2 = [(text_OT.get(), combo_cliente.get(), combo_proyecto.get(), values1, values2[0], values2[1], date_fechainicio.get_date().strftime("%d/%m/%Y"), date_fechacierre.get_date().strftime("%d/%m/%Y"), "Abierto")]
            # Definir la sentencia SQL para la inserción
            sql2 = '''INSERT INTO 'Proyectos Metalmecanica' (OT, Cliente, Proyecto, NoEnsamble, Ensamble, HorasBudget, FechaInicio, FechaCierre, Estatus)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            # Ejecutar la sentencia SQL con la lista de datos
            cursor.executemany(sql2, datos2)
            # Commit para guardar los cambios
            conexion.commit()
        
        messagebox.showinfo("Industria", "Datos actualizados con exito")

def limpiar():
    global NoEnsamble
    NoEnsamble = 0
    result = messagebox.askyesno("Confirmación", "¿Deseas borrar la informacion por capturar?")
    if result:
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)
        text_OT.configure(state="disabled") 
        combo_cliente.set("")
        combo_proyecto.set("")
        text_ensamble.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_ensamble.insert(0, "")
        text_ensamble.configure(state="disabled")
        text_budget.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_budget.insert(0, "")
        text_budget.configure(state="disabled")
        #combo_estatus.set("")
        #Limpiar el Treeview antes de insertar nuevos datos
        for item in Ensambles.get_children():
            Ensambles.delete(item)
        date_fechainicio.set_date(date.today().strftime("%d/%m/%Y"))
        date_fechacierre.set_date(date.today().strftime("%d/%m/%Y"))
        desbloquear_ensamble()
        desbloquear_botones()

def eliminar_operaciones():
        messagebox.showinfo("Industria", "Seleccione una operacion para eliminar")

def contador(event=None):
    print("contador")

#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("500x650")
ventana.configure(bg="#000040")
#ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

etiqueta_totalBuget = tk.Label(ventana, text="Budget total", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=15, height=1)
etiqueta_totalBuget.place(x=340, y=15)
etiqueta_OT = tk.Label(ventana, text="OT", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_OT.place(x=35, y=90)
etiqueta_cliente = tk.Label(ventana, text="Cliente", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_cliente.place(x=35, y=130)
etiqueta_proyecto = tk.Label(ventana, text="Proyecto", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_proyecto.place(x=35, y=170)
etiqueta_ensamble = tk.Label(ventana, text="Ensamble", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_ensamble.place(x=35, y=210)
etiqueta_horasbudget = tk.Label(ventana, text="Hrs Budget", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_horasbudget.place(x=30, y=250)
etiqueta_fechainicio = tk.Label(ventana, text="Inicio", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_fechainicio.place(x=35, y=540)
etiqueta_fechacierre = tk.Label(ventana, text="Cierre", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_fechacierre.place(x=35, y=580)
#etiqueta_estatus = tk.Label(ventana, text="Estatus", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
#etiqueta_estatus.place(x=35, y=620)
etiqueta_Guardarcambios = tk.Label(ventana, text="Guardar\ncambios", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=9, height=2)
etiqueta_Guardarcambios.place(x=375, y=245)
etiqueta_CrearOT = tk.Label(ventana, text="Generar OT", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=9, height=1)
etiqueta_CrearOT.place(x=305, y=595) 
etiqueta_Limpiar = tk.Label(ventana, text="Limpiar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Limpiar.place(x=395, y=595) 

text_totalBudget = tk.Entry(ventana, state="readonly", width=4, font=("Tahoma", 13), justify="center")
text_totalBudget.place(x=400, y=45)  
text_OT = tk.Entry(ventana, state="readonly", width=10, font=("Tahoma", 12))
text_OT.place(x=135, y=90)
text_ensamble = tk.Entry(ventana, state="disabled", width=25, font=("Tahoma", 12))
text_ensamble.place(x=135, y=210)
text_budget = tk.Entry(ventana, state="readonly", width=10, font=("Tahoma", 12))
text_budget.place(x=135, y=250)

date_fechainicio = DateEntry(ventana, width=12, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12))
date_fechainicio.place(x=135, y=540)
date_fechainicio.configure(date_pattern='dd/mm/yyyy')
date_fechacierre = DateEntry(ventana, width=12, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12))
date_fechacierre.place(x=135, y=580)
date_fechacierre.configure(date_pattern='dd/mm/yyyy')

combo_cliente = ttk.Combobox(ventana, values=clientes, state="normal", width=15, height=1, font=("Tahoma", 12))
combo_cliente.place(x=135, y=130)
combo_proyecto = ttk.Combobox(ventana, values=proyectos, state="normal", width=20, height=1, font=("Tahoma", 12))
combo_proyecto.place(x=135, y=170)
#combo_estatus = ttk.Combobox(ventana, values=Estatus, state="readonly", width=10, height=1, font=("Tahoma", 12))
#combo_estatus.place(x=135, y=620) 

Imagen_guardarcambios = tk.PhotoImage(file="guardar.png")
Guardar_cambios = tk.Button(ventana, state= "disabled", image=Imagen_guardarcambios, text="Agregar", command= guardar_cambios, width=50, height=50) 
Guardar_cambios.place(x=390, y=190)
Imagen_agregar = tk.PhotoImage(file="agregar.png")
Agregar_ensamble = tk.Button(ventana, state= "disabled", image=Imagen_agregar, text="Agregar", command= agregar_ensambles, width=25, height=25) 
Agregar_ensamble.place(x=250, y=247)
Imagen_eliminar_ensamble = tk.PhotoImage(file="menos.png")
Eliminar_ensamble = tk.Button(ventana, state= "disabled", image=Imagen_eliminar_ensamble, text="Borrar", command= eliminar_ensambles, width=25, height=25) 
Eliminar_ensamble.place(x=290, y=247)
Imagen_crearOT = tk.PhotoImage(file="crearOT.png")
Crear_OT = tk.Button(ventana, image=Imagen_crearOT, text="guardar", command=nuevo_proyecto, width=50, height=50)
Crear_OT.place(x=320, y=540)
Imagen_limpiar = tk.PhotoImage(file="limpiar.png")
Limpiar_proyecto = tk.Button(ventana, image=Imagen_limpiar, text="Limpiar", command=limpiar, width=50, height=50)
Limpiar_proyecto.place(x=400, y=540)

estilo_operaciones = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_operaciones.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_operaciones.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
Ensambles = ttk.Treeview(ventana, columns=(0, 1))
Ensambles.place(x=25, y=290)
# 5. Agregar encabezados
Ensambles.heading('#0', text='No')
Ensambles.column('#0', width=50, anchor="center")  # Ancho de la Columna 1
Ensambles.heading('#1', text='Ensamble')
Ensambles.column('#1', width=300, anchor="center")  # Ancho de la Columna 2
Ensambles.heading('#2', text='HorasB')
Ensambles.column('#2', width=75, anchor="center")  # Ancho de la Columna 2

#Inicio*****************************************************************************************************************************************************************************************
date_fechainicio.configure(state="disabled")
date_fechacierre.configure(state="disabled")
combo_cliente.bind("<<ComboboxSelected>>", filtro_clientes)
combo_cliente.bind("<KeyRelease>", filtro_clientes)
combo_proyecto.bind("<<ComboboxSelected>>", desbloquear_ensamble)
combo_proyecto.bind("<KeyRelease>", desbloquear_ensamble)
contador()

ventana.mainloop()