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

#Funciones***************************************************************************************************************************************************************************************

def contador(event):
    consulta1 = '''
    SELECT SUM("HorasNormales") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE OT = ? AND Proyecto = ?
    '''
    parametros1 = (combo_OT.get(), combo_proyecto.get())
    cursor.execute(consulta1, parametros1)
    resultados1 = cursor.fetchall()
    
    consulta2 = '''
    SELECT SUM("HorasExtra") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE OT = ? AND Proyecto = ?
    '''
    parametros2 = (combo_OT.get(), combo_proyecto.get())
    cursor.execute(consulta2, parametros2)
    resultados2 = cursor.fetchall()
    #print(resultados1[0][0])
    #print(resultados2[0][0])
    text_hrsProyecto.configure(state="normal")
    text_hrsProyectoExtras.configure(state="normal")
    if not resultados1[0][0]:
        text_hrsProyecto.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsProyecto.insert(0, 0)
    else:
        text_hrsProyecto.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsProyecto.insert(0, float(resultados1[0][0]))
    
    if not resultados2[0][0]:
        text_hrsProyectoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsProyectoExtras.insert(0, 0)
    else:
        text_hrsProyectoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsProyectoExtras.insert(0, float(resultados2[0][0]))
        text_hrsProyecto.configure(state="readonly")
        text_hrsProyectoExtras.configure(state="readonly")

def filtro_clientes(event):
    # Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT OT FROM `Proyectos Metalmecanica` WHERE Cliente = ?", (combo_cliente.get(),))
    ots = cursor.fetchall()
    # Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_OT['values'] = [ot[0] for ot in ots]
    
    # Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT Proyecto FROM `Proyectos Metalmecanica` WHERE Cliente = ?", (combo_cliente.get(),))
    proyectos = cursor.fetchall()
    # Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_proyecto['values'] = [proyecto[0] for proyecto in proyectos]
    contador("<<ComboboxSelected>>")

def filtro_proyectos(event):
    # Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT OT FROM `Proyectos Metalmecanica` WHERE Proyecto = ?", (combo_proyecto.get(),))
    ots = cursor.fetchall()
    # Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_OT['values'] = [ot[0] for ot in ots]
    combo_OT.set(str(ots[0]).strip("(',')"))

    # Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT Cliente FROM `Proyectos Metalmecanica` WHERE Proyecto = ?", (combo_proyecto.get(),))
    clientes = cursor.fetchall()
    # Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_cliente['values'] = [cliente[0] for cliente in clientes]
    combo_cliente.set(str(clientes[0]).strip("(',')"))

    query = '''
            SELECT E.NoEnsamble, E.Ensamble,
                COALESCE(SUM(DM.HorasNormales), 0) as TotalHorasNormales,
                COALESCE(SUM(DM.HorasExtra), 0) as TotalHorasExtra
            FROM 'Proyectos Metalmecanica' E
            LEFT JOIN "Datos Metalmecanica" DM ON E.Ensamble = DM.Ensamble
            WHERE E.OT = ? 
            GROUP BY E.NoEnsamble, E.Ensamble
            '''
    #Ejecutar la consulta con el valor de la fecha
    cursor.execute(query, (combo_OT.get(),))
    #Obtener los resultados
    resultados = cursor.fetchall()
    #Limpiar el Treeview antes de insertar nuevos datos
    for item in Ensambles.get_children():
        Ensambles.delete(item)
    #Insertar los resultados en el Treeview
    for resultado in resultados:
        Ensambles.insert("", "end", text=resultado[0], values=resultado[1:])
    
    try:
        cursor.execute("SELECT DISTINCT FechaInicio FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
        date_fechainicio.set_date(str(cursor.fetchall()).strip("[('',)]"))
        cursor.execute("SELECT DISTINCT FechaCierre FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
        date_fechacierre.set_date(str(cursor.fetchall()).strip("[('',)]"))

    except Exception as e:
        print(f"Error al obtener la fecha de cierre: {e}")

    cursor.execute("SELECT DISTINCT Estatus FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
    combo_estatus.set(str(cursor.fetchall()).strip("[('',)]"))
    text_ensamble.configure(state="normal")
    contador("<<ComboboxSelected>>")

def filtro_OT(event):
    #Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT Cliente FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
    clientes = cursor.fetchall()
    #Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_cliente['values'] = [cliente[0] for cliente in clientes]
    combo_cliente.set(clientes[0][0] if clientes else "")
    #combo_cliente.set(clientes)
    
    #Ejemplo de consulta a la base de datos
    cursor.execute("SELECT DISTINCT Proyecto FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
    proyectos = cursor.fetchall()
    #Obtener solo los valores de la columna 'Cliente' de la lista de tuplas y asignar los valores al Combobox
    combo_proyecto['values'] = [proyecto[0] for proyecto in proyectos]
    combo_proyecto.set(proyectos[0][0] if proyectos else "")
    #combo_proyecto.set(str(proyectos[0]).strip("(',')"))

    query = '''
            SELECT E.NoEnsamble, E.Ensamble,
                COALESCE(SUM(DM.HorasNormales), 0) as TotalHorasNormales,
                COALESCE(SUM(DM.HorasExtra), 0) as TotalHorasExtra
            FROM 'Proyectos Metalmecanica' E
            LEFT JOIN "Datos Metalmecanica" DM ON E.Ensamble = DM.Ensamble
            WHERE E.OT = ? 
            GROUP BY E.NoEnsamble, E.Ensamble
            '''
    #Ejecutar la consulta con el valor de la fecha
    cursor.execute(query, (combo_OT.get(),))
    resultados = cursor.fetchall()
    #Limpiar el Treeview antes de insertar nuevos datos
    for item in Ensambles.get_children():
        Ensambles.delete(item)
    #Insertar los resultados en el Treeview
    for resultado in resultados:
        Ensambles.insert("", "end", text=resultado[0], values=resultado[1:])
    
    try:
        cursor.execute("SELECT DISTINCT FechaInicio FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
        date_fechainicio.set_date(str(cursor.fetchall()).strip("[('',)]"))
        cursor.execute("SELECT DISTINCT FechaCierre FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
        date_fechacierre.set_date(str(cursor.fetchall()).strip("[('',)]"))

    except Exception as e:
        print(f"Error al obtener la fecha de cierre: {e}")

    cursor.execute("SELECT DISTINCT Estatus FROM `Proyectos Metalmecanica` WHERE OT = ?", (combo_OT.get(),))
    combo_estatus.set(str(cursor.fetchall()).strip("[('',)]"))
    text_ensamble.configure(state="normal")
    contador("<<ComboboxSelected>>")

def limpiar():
    result = messagebox.askyesno("Confirmación", "¿Deseas borrar la informacion por capturar?")
    if result: 
        combo_cliente.set("")
        combo_proyecto.set("")
        combo_OT.set("")
        text_ensamble.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_ensamble.insert(0, "")
        text_ensamble.configure(state="disabled") 
        combo_estatus.set("")
        Hoy = date.today()
        date_fechainicio.set_date(Hoy.strftime("%d/%m/%Y"))
        date_fechacierre.set_date(Hoy.strftime("%d/%m/%Y"))
        #Limpiar el Treeview antes de insertar nuevos datos
        for item in Ensambles.get_children():
            Ensambles.delete(item)
    contador("<<ComboboxSelected>>")

def eliminar_operaciones():
        messagebox.showinfo("Industria", "Seleccione una operacion para eliminar")

#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("550x650")
ventana.configure(bg="#000040")
#ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

etiqueta_Hrsacumuladas = tk.Label(ventana, text="Horas Acumuladas", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=15, height=1)
etiqueta_Hrsacumuladas.place(x=370, y=5)
etiqueta_Hrsnormales = tk.Label(ventana, text="Normales", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_Hrsnormales.place(x=360, y=60) 
etiqueta_Hrsextras = tk.Label(ventana, text="Extras", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=8, height=1)
etiqueta_Hrsextras.place(x=450, y=60)
etiqueta_OT = tk.Label(ventana, text="OT", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_OT.place(x=35, y=170)
etiqueta_cliente = tk.Label(ventana, text="Cliente", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_cliente.place(x=35, y=90)
etiqueta_proyecto = tk.Label(ventana, text="Proyecto", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_proyecto.place(x=35, y=130)
etiqueta_ensamble = tk.Label(ventana, text="Ensamble", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_ensamble.place(x=35, y=210)
etiqueta_fechainicio = tk.Label(ventana, text="Inicio", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_fechainicio.place(x=35, y=500)
etiqueta_fechacierre = tk.Label(ventana, text="Cierre", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_fechacierre.place(x=35, y=540)
etiqueta_estatus = tk.Label(ventana, text="Estatus", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_estatus.place(x=35, y=580)
etiqueta_Guardar = tk.Label(ventana, text="Guardar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Guardar.place(x=315, y=585) 
etiqueta_Limpiar = tk.Label(ventana, text="Limpiar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Limpiar.place(x=385, y=585)
etiqueta_Eliminar = tk.Label(ventana, text="Eliminar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Eliminar.place(x=455, y=585) 

text_hrsProyecto = tk.Entry(ventana, width=4, font=("Tahoma", 13), justify="center")
text_hrsProyecto.place(x=390, y=35) 
text_hrsProyectoExtras = tk.Entry(ventana, width=4, font=("Tahoma", 13), justify="center")
text_hrsProyectoExtras.place(x=470, y=35) 
text_ensamble = tk.Entry(ventana, state="normal", width=25, font=("Tahoma", 12))
text_ensamble.place(x=135, y=210)

date_fechainicio = DateEntry(ventana, width=12, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12))
date_fechainicio.place(x=135, y=500)
date_fechainicio.configure(date_pattern='dd/mm/yyyy')
date_fechacierre = DateEntry(ventana, width=12, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12))
date_fechacierre.place(x=135, y=540)
date_fechacierre.configure(date_pattern='dd/mm/yyyy')

combo_OT = ttk.Combobox(ventana, values=ots, state="normal", width=10, height=1, font=("Tahoma", 12))
combo_OT.place(x=135, y=170)
combo_cliente = ttk.Combobox(ventana, values=clientes, state="normal", width=15, height=1, font=("Tahoma", 12))
combo_cliente.place(x=135, y=90)
combo_proyecto = ttk.Combobox(ventana, values=proyectos, state="normal", width=20, height=1, font=("Tahoma", 12))
combo_proyecto.place(x=135, y=130)
combo_estatus = ttk.Combobox(ventana, values=Estatus, state="readonly", width=10, height=1, font=("Tahoma", 12))
combo_estatus.place(x=135, y=580) 

Imagen_agregar = tk.PhotoImage(file="agregar.png")
Agregar_ensamble = tk.Button(ventana, image=Imagen_agregar, text="Agregar", command= eliminar_operaciones, width=25, height=25) 
Agregar_ensamble.place(x=375, y=207)
Imagen_eliminar_ensamble = tk.PhotoImage(file="menos.png")
Eliminar_ensamble = tk.Button(ventana, image=Imagen_eliminar_ensamble, text="Borrar", command= eliminar_operaciones, width=25, height=25) 
Eliminar_ensamble.place(x=415, y=207)
Imagen_guardar = tk.PhotoImage(file="guardar.png")
Guardar_proyecto = tk.Button(ventana, image=Imagen_guardar, text="guardar", command=eliminar_operaciones, width=50, height=50)
Guardar_proyecto.place(x=320, y=530)
Imagen_limpiar = tk.PhotoImage(file="limpiar.png")
Limpiar_proyecto = tk.Button(ventana, image=Imagen_limpiar, text="Limpiar", command=limpiar, width=50, height=50)
Limpiar_proyecto.place(x=390, y=530)
Imagen_eliminar = tk.PhotoImage(file="borrar.png")
Eliminar_proyecto = tk.Button(ventana, image=Imagen_eliminar, text="Borrar", command= eliminar_operaciones, width=50, height=50) 
Eliminar_proyecto.place(x=460, y=530)

estilo_operaciones = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_operaciones.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_operaciones.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
Ensambles = ttk.Treeview(ventana, columns=(0, 1, 2))
Ensambles.place(x=25, y=250)
# 5. Agregar encabezados
Ensambles.heading('#0', text='No')
Ensambles.column('#0', width=50, anchor="center")  # Ancho de la Columna 1
Ensambles.heading('#1', text='Ensamble')
Ensambles.column('#1', width=300, anchor="center")  # Ancho de la Columna 2
Ensambles.heading('#2', text='HorasN')
Ensambles.column('#2', width=75, anchor="center")  # Ancho de la Columna 2
Ensambles.heading('#3', text='HorasE')
Ensambles.column('#3', width=75, anchor="center")  # Ancho de la Columna 2

#Inicio*****************************************************************************************************************************************************************************************

text_ensamble.configure(state="disabled")
contador("<<ComboboxSelected>>")
ventana.bind('<Motion>', contador)
combo_OT.bind("<<ComboboxSelected>>", filtro_OT)
combo_OT.bind("<KeyRelease>", filtro_OT)
combo_cliente.bind("<<ComboboxSelected>>", filtro_clientes)
combo_cliente.bind("<KeyRelease>", filtro_clientes)
combo_proyecto.bind("<<ComboboxSelected>>", filtro_proyectos)
combo_proyecto.bind("<KeyRelease>", filtro_proyectos)

ventana.mainloop()