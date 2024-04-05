import sqlite3
import tkinter as tk
import subprocess
import sys
from tkinter import ttk, messagebox, PhotoImage
from datetime import date, timedelta, datetime

#Valores iniciales******************************************************************************************************************************************************************************
conexion = sqlite3.connect('Breton industrial.db')  # Cambia el nombre del archivo de la base de datos si es diferente
cursor = conexion.cursor()
Fecha1 = ["Hoy", "Ayer", "Hace 2 dias", "Hace 3 dias"]
otros_proyectos = ["Supervisor", "Tiempo Muerto", "Salida a campo", "Fuera de proyecto", "Mantenimiento", "Hidraulica", "Falta", "Permiso", "Vacaciones", "Incidente"]
cursor.execute("SELECT Empleado FROM Empleados WHERE Departamento = 'Produccion'")
empleados = cursor.fetchall()
empleados = [empleado[0] for empleado in empleados]
#cursor.execute("SELECT DISTINCT Proyecto FROM `Proyectos Metalmecanica` WHERE Estatus = 'Abierto'")
#cursor.execute("SELECT DISTINCT Cliente || ', ' || Proyecto AS Cliente_Proyecto_Sumado FROM `Proyectos Metalmecanica` WHERE Estatus = 'Abierto'")
cursor.execute("SELECT DISTINCT Cliente || ', ' || Proyecto AS Cliente_Proyecto_Sumado FROM `Proyectos Metalmecanica` WHERE Estatus = 'Abierto' ORDER BY Cliente_Proyecto_Sumado")
proyectos = cursor.fetchall()
proyectos = [proyecto[0] for proyecto in proyectos]
proyectos = proyectos + otros_proyectos
ensambles = []
OT = " "
Horas = [0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10] 

#Funciones**************************************************************************************************************************************************************************************
def actualizar_fecha(event):
    Horario_regular['state'] = 'disabled'
    Extra_vespertino['state'] = 'disabled'
    Hoy = date.today()
    if combo_Fecha1.get() == "Hoy":
        text_fecha2.configure(state="normal")
        text_fecha2.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_fecha2.insert(0, Hoy.strftime("%d/%m/%Y"))
        text_fecha2.configure(state="readonly")
    elif combo_Fecha1.get() == "Ayer":
        text_fecha2.configure(state="normal")
        text_fecha2.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_fecha2.insert(0, (Hoy - timedelta(days=1)).strftime("%d/%m/%Y"))
        text_fecha2.configure(state="readonly")
    elif combo_Fecha1.get() == "Hace 2 dias":
        text_fecha2.configure(state="normal")
        text_fecha2.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_fecha2.insert(0, (Hoy - timedelta(days=2)).strftime("%d/%m/%Y"))
        text_fecha2.configure(state="readonly")
    elif combo_Fecha1.get() == "Hace 3 dias":
        text_fecha2.configure(state="normal")
        text_fecha2.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_fecha2.insert(0, (Hoy - timedelta(days=3)).strftime("%d/%m/%Y"))
        text_fecha2.configure(state="readonly")
    
    if datetime.strptime(text_fecha2.get(), "%d/%m/%Y").weekday() > 4:
        Horario_regular['state'] = 'disabled'
        Extra_vespertino['state'] = 'disabled'
    else:
        Horario_regular['state'] = 'normal'
        Extra_vespertino['state'] = 'normal'    
    contador("<<ComboboxSelected>>")

def actualizar_proyectos(event):
    combo_proyectos.configure(state="readonly")
    contador("<<ComboboxSelected>>")

def actualizar_ensambles(event):
    combo_ensambles['values'] = []
    if combo_proyectos.get() == "Fuera de proyecto" or combo_proyectos.get() == "Mantenimiento" or combo_proyectos.get() == "Hidraulica" or combo_proyectos.get() == "Salida a campo":
        OT = str("-")
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_OT.insert(0, OT[:5])  # Insertamos el resultado en el widget
        text_OT.configure(state="readonly")
        combo_ensambles.set("")
        combo_ensambles.configure(state="normal")
        Operaciones.set("-")
        for widget in Operaciones_frame.winfo_children():
            widget.configure(state="disabled")
    elif combo_proyectos.get() == "Supervisor" or combo_proyectos.get() == "Tiempo Muerto" or combo_proyectos.get() == "Falta" or combo_proyectos.get() == "Permiso" or combo_proyectos.get() == "Vacaciones" or combo_proyectos.get() == "Incidente":
        OT = str("-")
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_OT.insert(0, OT[:5])  # Insertamos el resultado en el widget
        text_OT.configure(state="readonly")
        combo_ensambles.set("-")
        Operaciones.set("-")
        for widget in Operaciones_frame.winfo_children():
            widget.configure(state="disabled")
    else:
        combo_ensambles.set("")
        combo_ensambles.configure(state="readonly")

        seleccion_proyecto = combo_proyectos.get()
        combo_ensambles.set('')
        cursor.execute("SELECT Ensamble FROM 'Proyectos Metalmecanica' WHERE Cliente || ', ' || Proyecto = ?", (seleccion_proyecto,))
        ensambles = cursor.fetchall()
        combo_ensambles['values'] = [ensamble[0] for ensamble in ensambles]

        seleccion_proyecto = combo_proyectos.get()
        cursor.execute("SELECT OT FROM 'Proyectos Metalmecanica' WHERE Cliente || ', ' || Proyecto = ?", (seleccion_proyecto,))
        resultado = cursor.fetchall()
        OT = str(resultado[0][0])
        #primeras_cinco_letras = OT[:5]
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_OT.insert(0, OT[:5])  # Insertamos el resultado en el widget
        text_OT.configure(state="readonly")

def desbloquear_frame(event):
    if combo_ensambles.get() == "-":
        Operaciones.set("-")
    else:
        for widget in Operaciones_frame.winfo_children():
            widget.configure(state="normal")

def horario_normal():
    combo_horasn.configure(state="readonly")
    combo_horase.set(0)
    combo_horase.configure(state="disabled")

def horario_extra():
    combo_horase.configure(state="readonly")
    combo_horasn.set(0)
    combo_horasn.configure(state="disabled")

def guardar():
    if combo_empleados.get() == "":
        messagebox.showinfo("Industria", "Favor de seleccionar un empleado")
        return
    elif combo_horasn.get() == "0" and combo_horase.get() == "0":
        messagebox.showinfo("Industria", "Favor de indicar una cantidad de horas")
        return
    
    if datetime.strptime(text_fecha2.get(), "%d/%m/%Y").weekday() == 4:
        #print("Es viernes")
        if float(text_HrsEmpleado.get()) + float(combo_horasn.get()) > 8:
            messagebox.showinfo("Industria", "No se pueden capturar mas de 8 HORAS REGULARES, revisa la captura por favor")
            return
    else:
        if float(text_HrsEmpleado.get()) + float(combo_horasn.get()) > 10:
            messagebox.showinfo("Industria", "No se pueden capturar mas de 10 HORAS REGULARES, revisa la captura por favor")
            return

    if combo_proyectos.get() == "":
        messagebox.showinfo("Industria", "Favor de seleccionar un proyecto")
        return
    elif combo_ensambles.get() == "":
        messagebox.showinfo("Industria", "Favor de seleccionar un ensamble")
        return
    elif Operaciones.get() == "ninguno":
        messagebox.showinfo("Industria", "Favor de seleccionar una operacion")
        return
    
    # Obtener el número de semana usando isocalendar
    #numero_semana = datetime.strptime(text_fecha2.get(), "%d/%m/%Y").isocalendar()[1]

    result = messagebox.askyesno("Confirmación", "¿Deseas guardar la informacion capturada?")
    if result:
        #print("Usuario seleccionó 'Yes'")
        # Definir una lista de datos a insertar
        datos = [(text_fecha2.get(), combo_empleados.get(), text_OT.get(), combo_proyectos.get(), combo_ensambles.get(), Operaciones.get(), Horario.get(), combo_horasn.get(), combo_horase.get(), str(datetime.strptime(text_fecha2.get(), "%d/%m/%Y").isocalendar()[1]) + str(datetime.strptime(text_fecha2.get(), "%d/%m/%Y").year), datetime.now().time().strftime('%H:%M:%S'), "No")]
        # Definir la sentencia SQL para la inserción
        sql = '''INSERT INTO 'Datos Metalmecanica' (Fecha, Empleado, OT, Proyecto, Ensamble, Operacion, Horario, HorasNormales, HorasExtra, Semana, HoraRegistro, Aprobadas)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        # Ejecutar la sentencia SQL con la lista de datos
        cursor.executemany(sql, datos)
        # Commit para guardar los cambios
        conexion.commit()
        messagebox.showinfo("Industria", "Datos Guardados con exito")
    else:
        #print("Usuario seleccionó 'No'")
        combo_empleados.focus_set()

    #if combo_ensambles.get() == "-":
    if text_OT.get() == "-":
        Operaciones.set("-")
    else:
        Operaciones.set("ninguno")

    Horario.set("ninguno")
    combo_horasn.set(0)
    combo_horase.set(0)
    combo_horasn.configure(state="disabled")
    combo_horase.configure(state="disabled")
    combo_ensambles.configure(state="readonly")
    contador("<<ComboboxSelected>>")

def limpiar():
    result = messagebox.askyesno("Confirmación", "¿Deseas borrar la informacion por capturar?")
    if result: 
        combo_empleados.set("")
        combo_proyectos.set("")
        text_OT.configure(state="normal")
        text_OT.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_OT.insert(0, "") 
        text_OT.configure(state="readonly")
        combo_ensambles['values'] = []
        combo_ensambles.set("")
        combo_ensambles.configure(state="readonly") 
        Operaciones.set("ninguno") 
        Horario.set("ninguno") 
        combo_horasn.set(0) 
        combo_horase.set(0)
        combo_Fecha1.set("Hoy")
        actualizar_fecha("<<ComboboxSelected>>")

        combo_proyectos.configure(state="disabled")
        combo_ensambles.configure(state="disabled")
        combo_horasn.configure(state="disabled")
        combo_horase.configure(state="disabled")
        for widget in Operaciones_frame.winfo_children():
            widget.configure(state="disabled")
        combo_empleados.focus_set()
    contador("<<ComboboxSelected>>")

def ver_actividades():
    #print(text_fecha2.get(), combo_empleados.get())
    if combo_empleados.get():
        subprocess.run(['python', 'Veroperaciones1.py', text_fecha2.get(), combo_empleados.get()])
    else:
        messagebox.showinfo("Industria", "Seleccione un empleado")

def contador(event):
    consulta1 = '''
    SELECT SUM("HorasNormales") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE Empleado = ? AND Fecha = ?
    '''
    parametros1 = (combo_empleados.get(), text_fecha2.get())
    cursor.execute(consulta1, parametros1)
    resultados1 = cursor.fetchall()
    
    consulta2 = '''
    SELECT SUM("HorasExtra") as Total_Horas_Normales
    FROM 'Datos Metalmecanica'
    WHERE Empleado = ? AND Fecha = ?
    '''
    parametros2 = (combo_empleados.get(), text_fecha2.get())
    cursor.execute(consulta2, parametros2)
    resultados2 = cursor.fetchall()
    #print(resultados1[0][0])
    #print(resultados2[0][0])
    text_HrsEmpleado.configure(state="normal")
    text_HrsEmpleadoExtras.configure(state="normal")
    if not resultados1[0][0]:
        text_HrsEmpleado.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_HrsEmpleado.insert(0, 0)
    else:
        text_HrsEmpleado.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_HrsEmpleado.insert(0, float(resultados1[0][0]))
    
    if not resultados2[0][0]:
        text_HrsEmpleadoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_HrsEmpleadoExtras.insert(0, 0)
    else:
        text_HrsEmpleadoExtras.delete(0, tk.END)  # Limpiamos el contenido del widget
        text_HrsEmpleadoExtras.insert(0, float(resultados2[0][0]))
    text_HrsEmpleado.configure(state="readonly")
    text_HrsEmpleadoExtras.configure(state="readonly")


#Interfaz***************************************************************************************************************************************************************************************
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("600x850")
ventana.configure(bg="#000040")
ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

# Etiquetas
etiqueta_Hrsacumuladas = tk.Label(ventana, text="Horas Acumuladas", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=15, height=1)
etiqueta_Hrsacumuladas.place(x=400, y=5)
etiqueta_Hrsnormales = tk.Label(ventana, text="Normales", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_Hrsnormales.place(x=380, y=60) 
etiqueta_Hrsextras = tk.Label(ventana, text="Extras", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=8, height=1)
etiqueta_Hrsextras.place(x=470, y=60) 
etiqueta_fecha = tk.Label(ventana, text="Fecha", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=5, height=1)
etiqueta_fecha.place(x=95, y=95)
etiqueta_empleados = tk.Label(ventana, text="Empleado", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1) 
etiqueta_empleados.place(x=54, y=130)
etiqueta_proyectos = tk.Label(ventana, text="Proyecto", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_proyectos.place(x=30, y=220)
etiqueta_OT = tk.Label(ventana, text="OT", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=2, height=1)
etiqueta_OT.place(x=430, y=220) 
etiqueta_ensambles = tk.Label(ventana, text="Ensambles", fg="white", font=("Tahoma", 12, "bold"), bg="#000040", width=10, height=1)
etiqueta_ensambles.place(x=24, y=255)
etiqueta_regular = tk.Label(ventana, text="Horario Regular", fg="white", font=("Tahoma", 10, "bold"), bg="#000040", width=12, height=1)
etiqueta_regular.place(x=65, y=174)
etiqueta_matutino = tk.Label(ventana, text="Extra Matutino", fg="white", font=("Tahoma", 10, "bold"), bg="#000040", width=13, height=1)
etiqueta_matutino.place(x=250, y=160)
etiqueta_vespertino = tk.Label(ventana, text="Extra Vespertino", fg="white", font=("Tahoma", 10, "bold"), bg="#000040", width=15, height=1)
etiqueta_vespertino.place(x=250, y=190)
etiqueta_Guardar = tk.Label(ventana, text="Guardar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Guardar.place(x=150, y=810) 
etiqueta_Limpiar = tk.Label(ventana, text="Limpiar", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_Limpiar.place(x=250, y=810) 
etiqueta_ver = tk.Label(ventana, text="Ver actividades", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=12, height=1)
etiqueta_ver.place(x=350, y=810)

# Textbox 
text_HrsEmpleado = tk.Entry(ventana, state= "readonly", width=4, font=("Tahoma", 13), justify="center")
text_HrsEmpleado.place(x=410, y=35) 
text_HrsEmpleadoExtras = tk.Entry(ventana, state= "readonly", width=4, font=("Tahoma", 13), justify="center")
text_HrsEmpleadoExtras.place(x=490, y=35) 
text_fecha2 = ttk.Entry(ventana, width=10, font=("Tahoma", 12))
text_fecha2.place(x=275, y=95)
text_OT = ttk.Entry(ventana, state= "readonly", width=7, font=("Tahoma", 12))
text_OT.place(x=465, y=220)

# ComboBox 
combo_Fecha1 = ttk.Combobox(ventana, values=Fecha1, state="readonly", width=10, height=1, font=("Tahoma", 12))
combo_Fecha1.place(x=155, y=95)
combo_empleados = ttk.Combobox(ventana, values=empleados, state="readonly", width=25, height=1, font=("Tahoma", 12))
combo_empleados.place(x=155, y=130) 
combo_proyectos = ttk.Combobox(ventana, values=proyectos, state="readonly", width=30, height=1, font=("Tahoma", 12))
combo_proyectos.place(x=130, y=220) 
combo_horasn = ttk.Combobox(ventana, values=Horas, state="readonly", width=3, height=1, font=("Tahoma", 12))
combo_horasn.place(x=175, y=174) 
combo_horase = ttk.Combobox(ventana, values=Horas, state="readonly", width=3, height=1, font=("Tahoma", 12))
combo_horase.place(x=380, y=174) 
combo_ensambles = ttk.Combobox(ventana, values=ensambles, state="readonly", width=30, height=1, font=("Tahoma", 12))
combo_ensambles.place(x=130, y=255) 

#Botones de horario
Horario = tk.StringVar(value="ninguno")
Horario_regular = tk.Radiobutton(ventana, variable=Horario, value="Regular", bg="#000040", command=horario_normal) 
Horario_regular.place(x=36, y=174) 
Extra_matutino = tk.Radiobutton(ventana, variable=Horario, value="Extra Matutino", bg="#000040", command=horario_extra) 
Extra_matutino.place(x=230, y=160) 
Extra_vespertino = tk.Radiobutton(ventana, variable=Horario, value="Extra Vespertino", bg="#000040", command=horario_extra) 
Extra_vespertino.place(x=230, y=190) 

#Botones
Imagen_guardar = tk.PhotoImage(file="guardar.png")
Guardar = tk.Button(ventana, image=Imagen_guardar, text="guardar", command=guardar, width=50, height=50)
Guardar.place(x=160, y=755)
Imagen_limpiar = tk.PhotoImage(file="limpiar.png")
Limpiar = tk.Button(ventana, image=Imagen_limpiar, text="Limpiar", command=limpiar, width=50, height=50)
Limpiar.place(x=260, y=755)
Imagen_ver = tk.PhotoImage(file="ver.png")
Borrar = tk.Button(ventana, image=Imagen_ver, text="Borrar", command=ver_actividades, width=50, height=50) 
Borrar.place(x=360, y=755)

#Ventana operaciones****************************************************************************************************************************************************************************
Operaciones_frame = tk.Frame(ventana, bg="light blue", width=550, height=450, borderwidth=2, relief="ridge")
Operaciones_frame.place(x=25, y=290)
Operaciones = tk.StringVar(value="ninguno")

#etiquetas
etiqueta_Operaciones = tk.Label(Operaciones_frame, text="Operaciones", fg="#800000", font=("Tahoma", 16, "bold"), bg="light blue", width=10, height=1)
etiqueta_Operaciones.place(x=0, y=0) 
etiqueta_Retrabajos = tk.Label(Operaciones_frame, text="Retrabajos", fg="#800000", font=("Tahoma", 16, "bold"), bg="light blue", width=10, height=1)
etiqueta_Retrabajos.place(x=350, y=0) 

#botones operaciones
Corte = tk.Radiobutton(Operaciones_frame, text="01-Corte", variable=Operaciones, value="Corte", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Corte.place(x=10, y=40) 
Movimientos = tk.Radiobutton(Operaciones_frame, text="02-Movimientos", variable=Operaciones, value="Movimientos", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Movimientos.place(x=10, y=70) 
Limpieza = tk.Radiobutton(Operaciones_frame, text="03-Limpieza", variable=Operaciones, value="Limpieza", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Limpieza.place(x=10, y=100) 
Laser = tk.Radiobutton(Operaciones_frame, text="04-Laser", variable=Operaciones, value="Laser", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Laser.place(x=10, y=130) 
Plasma = tk.Radiobutton(Operaciones_frame, text="05-Plasma", variable=Operaciones, value="Plasma", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Plasma.place(x=10, y=160) 
Oxycorte = tk.Radiobutton(Operaciones_frame, text="06-Oxycorte", variable=Operaciones, value="Oxycorte", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Oxycorte.place(x=10, y=190) 
Perfilado = tk.Radiobutton(Operaciones_frame, text="07-Perfilado", variable=Operaciones, value="Perfilado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Perfilado.place(x=10, y=220) 
Rolado = tk.Radiobutton(Operaciones_frame, text="08-Rolado", variable=Operaciones, value="Rolado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Rolado.place(x=10, y=250) 
Barrenado = tk.Radiobutton(Operaciones_frame, text="09-Barrenado", variable=Operaciones, value="Barrenado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Barrenado.place(x=10, y=280) 
Ponchado = tk.Radiobutton(Operaciones_frame, text="10-Ponchado", variable=Operaciones, value="Ponchado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Ponchado.place(x=10, y=310) 
Machuelado = tk.Radiobutton(Operaciones_frame, text="11-Machuelado", variable=Operaciones, value="Machuelado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Machuelado.place(x=10, y=340) 
Maquinado = tk.Radiobutton(Operaciones_frame, text="12-Maquinado", variable=Operaciones, value="Maquinado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Maquinado.place(x=10, y=370) 
Armado = tk.Radiobutton(Operaciones_frame, text="13-Armado", variable=Operaciones, value="Armado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Armado.place(x=170, y=40) 
Soldadura = tk.Radiobutton(Operaciones_frame, text="14-Soladura", variable=Operaciones, value="Soldadura", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Soldadura.place(x=170, y=70) 
Acabado = tk.Radiobutton(Operaciones_frame, text="15-Acabado", variable=Operaciones, value="Acabado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Acabado.place(x=170, y=100) 
Fabricacion = tk.Radiobutton(Operaciones_frame, text="16-Fabricacion", variable=Operaciones, value="Fabricacion", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Fabricacion.place(x=170, y=130) 
Instalacion = tk.Radiobutton(Operaciones_frame, text="17-Instalacion", variable=Operaciones, value="Instalacion", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Instalacion.place(x=170, y=160) 
Enderezado = tk.Radiobutton(Operaciones_frame, text="18-Enderezado", variable=Operaciones, value="Enderezado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Enderezado.place(x=170, y=190) 
Pruebas = tk.Radiobutton(Operaciones_frame, text="19-Pruebas", variable=Operaciones, value="Pruebas", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Pruebas.place(x=170, y=220) 
Ensamblefinal = tk.Radiobutton(Operaciones_frame, text="20-Ensamble Final", variable=Operaciones, value="Ensamble final", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Ensamblefinal.place(x=170, y=250) 
Limpieza = tk.Radiobutton(Operaciones_frame, text="21-Lavado", variable=Operaciones, value="Limpieza", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Limpieza.place(x=170, y=280) 
Pintura = tk.Radiobutton(Operaciones_frame, text="22-Pintura", variable=Operaciones, value="Pintura", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Pintura.place(x=170, y=310) 
Enviado = tk.Radiobutton(Operaciones_frame, text="23-Enviado", variable=Operaciones, value="Enviado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
Enviado.place(x=170, y=340)

RetCorte = tk.Radiobutton(Operaciones_frame, text="24-RetCorte", variable=Operaciones, value="Retrabajo de corte", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
RetCorte.place(x=340, y=40) 
RetSoldadura = tk.Radiobutton(Operaciones_frame, text="25-RetSoldadura", variable=Operaciones, value="Retrabajo de soldadura", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
RetSoldadura.place(x=340, y=70) 
RetArmado = tk.Radiobutton(Operaciones_frame, text="26-RetArmado", variable=Operaciones, value="Retrabajo de armado", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
RetArmado.place(x=340, y=100) 
RetPintura = tk.Radiobutton(Operaciones_frame, text="27-RetPintura", variable=Operaciones, value="Retrabajo de pintura", fg="black", font=("Tahoma", 11, "bold"), bg="light blue") 
RetPintura.place(x=340, y=130) 

#Inicio*****************************************************************************************************************************************************************************************
combo_Fecha1.set(Fecha1[0])
combo_proyectos.configure(state="disabled")
combo_ensambles.configure(state="disabled")
combo_horasn.set(0)
combo_horase.set(0)
combo_horasn.configure(state="disabled")
combo_horase.configure(state="disabled")

for widget in Operaciones_frame.winfo_children():
    widget.configure(state="disabled")

contador("<<ComboboxSelected>>")
actualizar_fecha("<<ComboboxSelected>>")
combo_Fecha1.bind("<<ComboboxSelected>>", actualizar_fecha)
combo_empleados.bind("<<ComboboxSelected>>",actualizar_proyectos)
combo_proyectos.bind("<<ComboboxSelected>>", actualizar_ensambles)
combo_ensambles.bind("<<ComboboxSelected>>", desbloquear_frame)
ventana.bind('<Motion>', contador)

ventana.mainloop()