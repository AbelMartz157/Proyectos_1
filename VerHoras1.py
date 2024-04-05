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
cursor.execute('SELECT DISTINCT Departamento FROM Empleados')
departamentos = cursor.fetchall()
departamentos = [departamento[0] for departamento in departamentos]

#Funciones**************************************************************************************************************************************************************************************
def ver_operaciones(event=None):
    #print(Fecha.get_date().strftime('%d/%m/%Y'))
    if combo_departamento.get():
        # Consulta SQL con LEFT JOIN y filtrado por fecha
        query1 = '''
            SELECT E.Empleado,
                COALESCE(SUM(DM.HorasNormales), 0) as TotalHorasNormales,
                COALESCE(SUM(DM.HorasExtra), 0) as TotalHorasExtra,
                CASE WHEN MIN(DM.Aprobadas = 'Si') = 1 THEN 'Si' ELSE 'No' END as TotalAprobadas
            FROM Empleados E
            LEFT JOIN "Datos Metalmecanica" DM ON E.Empleado = DM.Empleado AND DM.Fecha = ?
            WHERE E.Departamento = ? 
            GROUP BY E.Empleado
        '''

        # Ejecutar la consulta con el valor de la fecha
        cursor.execute(query1, (date_fecha.get_date().strftime('%d/%m/%Y'), combo_departamento.get()))

        # Obtener los resultados
        resultados = cursor.fetchall()

        # Limpiar el Treeview antes de insertar nuevos datos
        for item in Operaciones.get_children():
            Operaciones.delete(item)

        # Insertar los resultados en el Treeview y aplicar etiquetas de color
        for row in resultados:
            Operaciones.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))
            Operaciones.item(Operaciones.get_children()[-1], tags=("grande"))
            
            # Aplicar etiquetas de color
            if datetime.strptime(date_fecha.get_date().strftime("%d/%m/%Y"), "%d/%m/%Y").weekday() == 4:
                #print("Es viernes")
                if row[1] < 8:
                    Operaciones.item(Operaciones.get_children()[-1], tags=("grande","rojo"))
            elif datetime.strptime(date_fecha.get_date().strftime("%d/%m/%Y"), "%d/%m/%Y").weekday() == 5:
                #print("Es sabado")
                if row[2] == 0:
                    Operaciones.item(Operaciones.get_children()[-1], tags=("grande","rojo"))
            elif datetime.strptime(date_fecha.get_date().strftime("%d/%m/%Y"), "%d/%m/%Y").weekday() == 6:
                #print("Es domingo")
                if row[2] == 0:
                    Operaciones.item(Operaciones.get_children()[-1], tags=("grande","rojo"))
            else:
                if row[1] < 10:
                    Operaciones.item(Operaciones.get_children()[-1], tags=("grande","rojo"))
            
            if row[3] == "Si":
                    Operaciones.item(Operaciones.get_children()[-1], tags=("grande","verde"))

            #if row[1] == 0 and row[2] == 0:
                #Operaciones.item(Operaciones.get_children()[-1], tags=("rojo"))

    else:
        #print("No se proporcionó suficiente información.")
        messagebox.showinfo("Industria", "Seleccione un departamento")

def cambio_fecha(event):
    for item in Operaciones.get_children():
            Operaciones.delete(item)

def on_double_click(event):
    try:
        item = Operaciones.selection()[0]  # Obtener el elemento seleccionado
        # Aquí puedes llamar a la función que deseas ejecutar al dar doble clic
        Empleado = Operaciones.item(item, 'text')
        #print(f"Doble clic en {Empleado}")
        if Empleado:
            subprocess.run(['python', 'Aprobaroperaciones1.py', date_fecha.get_date().strftime('%d/%m/%Y'), Empleado])
        else:
            messagebox.showinfo("Industria", "Seleccione un empleado")
    
    except IndexError:
        #print("Selecciona un empleado")
        messagebox.showinfo("Industria", "Seleccione un empleado")

#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("650x480")
ventana.configure(bg="#000040")
ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

etiqueta_fecha = tk.Label(ventana, text="Fecha", fg="white", font=("Tahoma", 15, "bold"), bg="#000040", width=5, height=1)
etiqueta_fecha.place(x=35, y=95)
etiqueta_departamento = tk.Label(ventana, text="Departamento", fg="white", font=("Tahoma", 15, "bold"), bg="#000040", width=11, height=1)
etiqueta_departamento.place(x=35, y=140)
etiqueta_actualizar = tk.Label(ventana, text="Actualizar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
#etiqueta_actualizar.place(x=525, y=160)

date_fecha = DateEntry(ventana, width=10, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12))
date_fecha.place(x=110, y=100)
date_fecha.configure(date_pattern='dd/mm/yyyy')

combo_departamento = ttk.Combobox(ventana, values=departamentos, state="readonly", width=14, height=1, font=("Tahoma", 12))
combo_departamento.place(x=190, y=145)

#Imagen_actualizar = tk.PhotoImage(file="actualizar.png")
#Actualizar = tk.Button(ventana, image=Imagen_actualizar, text="Borrar", command= ver_operaciones, width=50, height=50) 
#Actualizar.place(x=530, y=100)

estilo_operaciones = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_operaciones.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_operaciones.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
Operaciones = ttk.Treeview(ventana, columns=(0, 1, 2))
Operaciones.place(x=35, y=200)
# 5. Agregar encabezados
Operaciones.heading('#0', text='Empleado')
Operaciones.column('#0', width=250)  # Ancho de la Columna 1
Operaciones.heading('#1', text='HorasN')
Operaciones.column('#1', width=100, anchor="center")  # Ancho de la Columna 4
Operaciones.heading('#2', text='HorasE')
Operaciones.column('#2', width=100, anchor="center")
Operaciones.heading('#3', text='Aprobadas')
Operaciones.column('#3', width=100, anchor="center")
Operaciones.tag_configure("grande", font=('Arial', 11))
Operaciones.tag_configure("rojo", background="red")
Operaciones.tag_configure("verde", background="lightgreen")
scroll_y = ttk.Scrollbar(ventana, orient="vertical", command=Operaciones.yview)
scroll_y.place(x=587, y=230, height=203)  # Ajusta la posición y altura según tus necesidades
Operaciones.configure(yscrollcommand=scroll_y.set)


#Inicio*****************************************************************************************************************************************************************************************
date_fecha.bind("<<DateEntrySelected>>", ver_operaciones)
combo_departamento.set("Produccion")
ver_operaciones()
ventana.bind('<Motion>', ver_operaciones)
combo_departamento.bind("<<ComboboxSelected>>", ver_operaciones)
# Configurar el evento de doble clic
Operaciones.bind("<Double-1>", on_double_click)

ventana.mainloop()