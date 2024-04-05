import sqlite3
import tkinter as tk
import subprocess
import sys
from tkinter import ttk, messagebox, PhotoImage
from datetime import date, timedelta, datetime
from tkcalendar import DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#Valores iniciales******************************************************************************************************************************************************************************

#Funciones**************************************************************************************************************************************************************************************
def exportar_a_pdf():
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Crear el nombre del archivo con la fecha y hora
    nombre_archivo = f"Reporte_Bono_Comida_{fecha_hora_actual}.pdf"
    
    pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

    # Insertar imagen en la esquina superior izquierda
    ruta_imagen = "Breton_industrial2.png"  # Reemplaza con la ruta de tu imagen
    pdf.drawImage(ruta_imagen, x=10, y=letter[1] - 60, width=250, height=50)

    # Obtener los datos del Treeview
    encabezados = ['Empleado', 'Horas trabajadas', 'Bono Comida']
    #datos = [bonocomida.item(item)["values"] for item in bonocomida.get_children()]
    datos = [[bonocomida.item(row_id, "text")] + [bonocomida.set(row_id, column) for column in bonocomida["columns"]] for row_id in bonocomida.get_children()]
    
    # Definir las posiciones iniciales
    x_inicial = 50
    y_inicial = 700
    ancho_columna = 200

    # Establecer el formato para el encabezado
    pdf.setFont("Helvetica-Bold", 12)
    #pdf.setFillColorRGB(0, 128, 0)  # Color verde (RGB)

    # Dibujar los encabezados
    for i, encabezado in enumerate(encabezados):
        pdf.drawString(x_inicial + i * ancho_columna, y_inicial, encabezado)

    # Restaurar el formato por defecto
    pdf.setFont("Helvetica", 12)
    pdf.setFillColorRGB(0, 0, 0)  # Restaurar el color de texto negro

    # Dibujar los datos
    y_inicial -= 20
    for fila in datos:
    # Verificar si el valor en la tercera columna es 'si'
        pintar_verde = fila[2].lower() == 'si'
        for i, valor in enumerate(fila):
            # Cambiar el color del texto a verde si se cumple la condición
            if pintar_verde:
                pdf.setFillColorRGB(0, 50, 0)
            pdf.drawString(x_inicial + i * ancho_columna, y_inicial, str(valor))
            # Restaurar el color de texto a negro después de dibujar cada elemento
            pdf.setFillColorRGB(0, 0, 0)
        y_inicial -= 15

    # Agregar el string al final del PDF
    pdf.setFont("Helvetica-Bold", 10)
    pdf.setFillColorRGB(255, 0, 0)  # Color rojo (RGB)
    pdf.drawString(x_inicial, y_inicial - 20, "*No aplican horas extra matutino")
    pdf.setFillColorRGB(0, 0, 0)  # Restaurar el color de texto negro

    # Guardar el archivo PDF
    pdf.save()

def calcular_si_no(total_horas):
    if total_horas >= 12:
        return "Si"
    else:
        return "No"

def bono_comida(event=None):
    # Obtener la fecha desde el widget de entrada
    #fecha = date_entry_fecha.get_date()

    # Formatear la fecha para que coincida con el formato de la base de datos (si es necesario)
    #fecha_formateada = date_fecha.get_date().strftime("%d/%m/%Y")

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('Breton Industrial.db')
    cursor = conn.cursor()
    
    if datetime.strptime(date_fecha.get(), "%d/%m/%Y").weekday() > 4: #Sabado, Domingo
        query = f"""
        SELECT Empleado, SUM(HorasNormales) + SUM(HorasExtra) AS TotalHoras
        FROM 'Datos Metalmecanica'
        WHERE Proyecto NOT IN ('Permiso', 'Falta') AND Fecha = ?
        GROUP BY Empleado;
        """
        cursor.execute(query, (date_fecha.get(),))
        resultados = cursor.fetchall()
        print("findesemana")
    else:
        # Ejecutar la consulta SQL
        query = f"""
        SELECT Empleado, SUM(HorasNormales) + SUM(HorasExtra) AS TotalHoras
        FROM 'Datos Metalmecanica'
        WHERE Proyecto NOT IN ('Permiso', 'Falta') AND Horario NOT IN ('Extra Matutino') AND Fecha = ?
        GROUP BY Empleado;
        """
        cursor.execute(query, (date_fecha.get(),))
        resultados = cursor.fetchall()
        print("entresemana")
    # Limpiar el Treeview antes de actualizar con nuevos resultados
    for row in bonocomida.get_children():
        bonocomida.delete(row)

    # Actualizar el Treeview con los nuevos resultados
    for resultado in resultados:
        total_horas = resultado[1]  # Obtener el valor de TotalHoras de la tupla resultado
        si_no = calcular_si_no(total_horas)
        resultado_con_si_no = resultado + (si_no,)  # Agregar el valor Si/No como una tupla adicional
        #bonocomida.insert("", "end", values=resultado_con_si_no)
        bonocomida.insert("", "end", text=resultado_con_si_no[0], values=(resultado_con_si_no[1], resultado_con_si_no[2]))
        bonocomida.item(bonocomida.get_children()[-1], tags=("grande"))
        if resultado_con_si_no[2] == "Si":
            bonocomida.item(bonocomida.get_children()[-1], tags=("grande","verde"))

    # Cerrar la conexión a la base de datos
    conn.close()

#Interfaz***************************************************************************************************************************************************************************************
# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Breton Industrial")
ventana.geometry("580x500")
ventana.configure(bg="#000040")
ventana.resizable(False, False)

Logo = PhotoImage(file="Breton_industrial.png")
Logo = Logo.subsample(4, 4)
#Logo = Logo.zoom(4, 4)
etiqueta = tk.Label(ventana, image=Logo)
etiqueta.place(x=15, y=15)

# Crear un widget DateEntry para seleccionar la fecha
etiqueta_fecha = tk.Label(ventana, text="Fecha", fg="white", font=("Tahoma", 15, "bold"), bg="#000040", width=5, height=1)
etiqueta_fecha.place(x=35, y=95)
etiqueta_nota = tk.Label(ventana, text="*No aplica el tiempo extra matutino", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=30, height=1)
etiqueta_nota.place(x=35, y=395)
etiqueta_imprimir = tk.Label(ventana, text="Imprimir", fg="white", font=("Tahoma", 12, "normal"), bg="#000040", width=7, height=1)
etiqueta_imprimir.place(x=465, y=460)

date_fecha = DateEntry(ventana, width=10, state="readonly", background='darkblue', foreground='white', borderwidth=3, font=("Tahoma", 12), date_pattern='dd/mm/yyyy')
date_fecha.place(x=110, y=100)

Imagen_imprimir = tk.PhotoImage(file="imprimir.png")
Imprimir = tk.Button(ventana, image=Imagen_imprimir, command=exportar_a_pdf, text="Borrar", width=50, height=50) 
Imprimir.place(x=470, y=400)

estilo_bonocomida = ttk.Style()
# Asegúrate de que estás utilizando un tema que permita personalizaciones
estilo_bonocomida.theme_use('clam')  # Puedes probar con otros temas si es necesario
# Personalizar el estilo de los encabezados
estilo_bonocomida.configure("Treeview.Heading", background="#808080", foreground="white", font=('Helvetica', 12, 'bold'))
bonocomida = ttk.Treeview(ventana, columns=(0, 1, 2))

# Crear un bonocomidaview para mostrar los resultados
bonocomida = ttk.Treeview(ventana, columns=(0, 1))
bonocomida.heading("#0", text="Empleado")
bonocomida.column('#0', width=200)
bonocomida.heading("#1", text="Horas trabajadas")
bonocomida.column('#1', width=150, anchor="center")
bonocomida.heading("#2", text="Bono Comida")
bonocomida.column('#2', width=150, anchor="center")
bonocomida.tag_configure("grande", font=('Arial', 11))
bonocomida.tag_configure("verde", background="lightgreen")
scroll_y = ttk.Scrollbar(ventana, orient="vertical", command=bonocomida.yview)
scroll_y.place(x=538, y=180, height=203)
bonocomida.configure(yscrollcommand=scroll_y.set)
bonocomida.place(x=35, y=150)

#Inicio*****************************************************************************************************************************************************************************************
# Ejecutar la interfaz gráfica
date_fecha.bind("<<DateEntrySelected>>", bono_comida)
bono_comida()

ventana.mainloop()
