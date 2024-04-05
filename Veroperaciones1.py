import sqlite3
import tkinter as tk
import subprocess
import sys
from tkinter import ttk, messagebox, PhotoImage
from datetime import date, timedelta, datetime

#Valores iniciales******************************************************************************************************************************************************************************
conexion = sqlite3.connect('Breton industrial.db')  # Cambia el nombre del archivo de la base de datos si es diferente
cursor = conexion.cursor()

#Funciones**************************************************************************************************************************************************************************************
def contador():
    consulta1 = '''
    SELECT SUM("HorasNormales") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE Empleado = ? AND Fecha = ?
    '''
    parametros1 = (text_empleado.get(), text_fecha.get())
    cursor.execute(consulta1, parametros1)
    resultados1 = cursor.fetchall()
    
    consulta2 = '''
    SELECT SUM("HorasExtra") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE Empleado = ? AND Fecha = ?
    '''
    parametros2 = (text_empleado.get(), text_fecha.get())
    cursor.execute(consulta2, parametros2)
    resultados2 = cursor.fetchall()
    #print(resultados1[0][0])
    #print(resultados2[0][0])
    text_hrsEmpleado.configure(state="normal")
    text_hrsEmpleadoExtras.configure(state="normal")
    if not resultados1[0][0]:
        text_hrsEmpleado.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsEmpleado.insert(0, 0)
    else:
        text_hrsEmpleado.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsEmpleado.insert(0, float(resultados1[0][0]))
    
    if not resultados2[0][0]:
        text_hrsEmpleadoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsEmpleadoExtras.insert(0, 0)
    else:
        text_hrsEmpleadoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_hrsEmpleadoExtras.insert(0, float(resultados2[0][0]))
    text_hrsEmpleado.configure(state="readonly")
    text_hrsEmpleadoExtras.configure(state="readonly")

def ver_operaciones():
    cursor.execute("SELECT Proyecto, Ensamble, Operacion, Horario, HorasNormales, HorasExtra FROM 'Datos Metalmecanica' WHERE Empleado = ? AND Fecha = ?", (text_empleado.get(), text_fecha.get()))
    datos_filtrados = cursor.fetchall()
    for dato in datos_filtrados:
        Operaciones.insert("", "end", text=dato[0], values=dato[1:])
        Operaciones.item(Operaciones.get_children()[-1], tags=("grande"))
    #for col in Operaciones["columns"]:
        #Operaciones.column(col, anchor="center")  # Centrar contenido

def eliminar_operaciones():
    try:
        result = messagebox.askyesno("Confirmación", "¿Deseas eliminar la informacion seleccionada?")
        #print(f"Empleado: {text_empleado.get()}, Fecha: {text_fecha.get()}")
        item = Operaciones.focus()  # Obtiene el elemento seleccionado
        datos_seleccionados = Operaciones.item(item, "values")
        #print(item)
        
        #Consulta sqlite
        cursor.execute("DELETE FROM 'Datos Metalmecanica' WHERE Fecha = ? AND Empleado = ? AND Proyecto = ? AND Ensamble = ? AND Operacion = ? AND Horario = ? AND HorasNormales = ? AND HorasExtra = ?", 
        (text_fecha.get(), text_empleado.get(), Operaciones.item(item, "text"), datos_seleccionados[0], datos_seleccionados[1], datos_seleccionados[2], datos_seleccionados[3], datos_seleccionados[4]))
        
        
        if result:    
            #Guardar resultados eliminados
            conexion.commit()
            Operaciones.delete(*Operaciones.get_children())
            ver_operaciones()
            contador()
            
    except IndexError:
        messagebox.showinfo("Industria", "Seleccione una operacion para eliminar")

#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("1100x475")
ventana.configure(bg="#000040")
ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

etiqueta_Hrsacumuladas = tk.Label(ventana, text="Horas Acumuladas", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=15, height=1)
etiqueta_Hrsacumuladas.place(x=890, y=5)
etiqueta_Hrsnormales = tk.Label(ventana, text="Normales", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_Hrsnormales.place(x=880, y=60) 
etiqueta_Hrsextras = tk.Label(ventana, text="Extras", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=8, height=1)
etiqueta_Hrsextras.place(x=970, y=60)
etiqueta_fecha = tk.Label(ventana, text="Fecha", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=5, height=1)
etiqueta_fecha.place(x=95, y=95)
etiqueta_empleados = tk.Label(ventana, text="Empleado", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_empleados.place(x=54, y=130)
etiqueta_eliminar = tk.Label(ventana, text="Eliminar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_eliminar.place(x=980, y=160)

text_hrsEmpleado = tk.Entry(ventana, width=4, font=("Tahoma", 13))
text_hrsEmpleado.place(x=910, y=35) 
text_hrsEmpleadoExtras = tk.Entry(ventana, width=4, font=("Tahoma", 13))
text_hrsEmpleadoExtras.place(x=990, y=35) 
text_fecha = tk.Entry(ventana, state="readonly", width=10, font=("Tahoma", 12))
text_fecha.place(x=155, y=95)
text_empleado = tk.Entry(ventana, state="readonly", width=25, font=("Tahoma", 12))
text_empleado.place(x=155, y=130) 

Imagen_eliminar = tk.PhotoImage(file="borrar.png")
Eliminar = tk.Button(ventana, image=Imagen_eliminar, text="Borrar", command= eliminar_operaciones, width=50, height=50) 
Eliminar.place(x=985, y=100)

estilo_operaciones = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_operaciones.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_operaciones.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
Operaciones = ttk.Treeview(ventana, columns=(0, 1, 2, 3, 4))
Operaciones.place(x=30, y=200)
# 5. Agregar encabezados
Operaciones.heading('#0', text='Proyecto')
Operaciones.column('#0', width=250, anchor="center")  # Ancho de la Columna 1
Operaciones.heading('#1', text='Ensamble')
Operaciones.column('#1', width=200, anchor="center")  # Ancho de la Columna 2
Operaciones.heading('#2', text='Operacion')
Operaciones.column('#2', width=175, anchor="center")  # Ancho de la Columna 3
Operaciones.heading('#3', text='Horario')
Operaciones.column('#3', width=200, anchor="center")  # Ancho de la Columna 4
Operaciones.heading('#4', text='HorasN')
Operaciones.column('#4', width=100, anchor="center")  # Ancho de la Columna 4
Operaciones.heading('#5', text='HorasE')
Operaciones.column('#5', width=100, anchor="center")
Operaciones.tag_configure("grande", font=('Arial', 11))
scroll_y = ttk.Scrollbar(ventana, orient="vertical", command=Operaciones.yview)
scroll_y.place(x=1057, y=230, height=203)

#Inicio*****************************************************************************************************************************************************************************************
try:
    #print(sys.argv[1], sys.argv[2])
    text_fecha.configure(state="normal")
    text_fecha.delete(0, tk.END)  # Limpiamos el contenido del widget
    text_fecha.insert(0, sys.argv[1])
    text_fecha.configure(state="readonly")

    text_empleado.configure(state="normal")
    text_empleado.delete(0, tk.END)  # Limpiamos el contenido del widget
    text_empleado.insert(0, sys.argv[2])
    text_empleado.configure(state="readonly")

except IndexError:
    print("No se proporcionó suficiente información.")

ver_operaciones()
contador()

ventana.mainloop()