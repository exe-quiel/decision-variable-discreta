import tkinter as tk
import tkinter.simpledialog
from tkinter.ttk import Notebook, Combobox, Style, Separator
from table import DoubleEntryTable

from criterios import *

window = tk.Tk()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650
WINDOW_POS_X = window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2
WINDOW_POS_Y = window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2

#window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.geometry(f'+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.title('Analizador')

frame_principal = tk.Frame(window)

def regenerar_analisis(sheet, parent_frame):
    global wald_frame
    global maximax_frame
    global frame_hurwicz
    global frame_savage
    global frame_esperanza

    coeficiente_hurwicz = frame_hurwicz.get_coeficiente()
    probabilidades_esperanza = frame_esperanza.get_probabilidades()
    usar_laplace_esperanza = frame_esperanza.is_usar_laplace()

    wald_frame.destroy()
    maximax_frame.destroy()
    frame_hurwicz.destroy()
    frame_savage.destroy()
    frame_esperanza.destroy()

    wald_frame = Wald(parent_frame, sheet.get_values_as_list(), sheet.get_row_headers())
    wald_frame.grid(column=0, row=0, sticky=tk.NSEW)

    maximax_frame = Maximax(parent_frame, sheet.get_values_as_list(), sheet.get_row_headers())
    maximax_frame.grid(column=1, row=0, sticky=tk.NSEW)

    frame_hurwicz = Hurwicz(parent_frame, sheet.get_values_as_list(), sheet.get_row_headers(), coeficiente_hurwicz)
    frame_hurwicz.grid(column=0, row=1, sticky=tk.NSEW)

    frame_savage = Savage(parent_frame, sheet.get_values_as_list(), sheet.get_row_headers(), sheet.get_column_headers())
    frame_savage.grid(column=1, row=1, sticky=tk.NSEW)

    frame_esperanza = Esperanza(parent_frame, sheet.get_values_as_list(), sheet.get_row_headers(), sheet.get_column_headers(), probabilidades_esperanza, usar_laplace_esperanza)
    frame_esperanza.grid(column=0, row=2, columnspan=2, sticky=tk.NSEW)

## Datos

frame_datos = tk.LabelFrame(frame_principal, width=5, text='Datos', padx=5, pady=5)
frame_datos.grid(column=0, row=0, sticky=tk.NSEW)

frame_datos.columnconfigure(0, weight=1)
frame_datos.columnconfigure(1, weight=1)
frame_datos.columnconfigure(2, weight=1)

matriz, _, _ = cargar_matriz_ejercicio()
headers_columnas = ['Muy bueno', 'Bueno', 'Regular', 'Malo']
headers_filas = ['Grande', 'Mediana', 'Chica', 'Nada']

def read_str_and_replace_header(event):
    new_text = tk.simpledialog.askstring('Nuevo texto', 'Ingresar nuevo texto')
    event.widget['text'] = new_text

sheet = DoubleEntryTable(frame_datos, matriz, headers_columnas, headers_filas, read_str_and_replace_header)
sheet.grid(column=0, row=0)

sheet_config_frame = tk.Frame(frame_datos)

def handle_col_spinbox():
    global filas_spinbox
    global matriz
    global headers_columnas
    global sheet
    n_col_nuevo = int(columnas_spinbox.get())
    print(f'n_col_nuevo: {n_col_nuevo} | len(matriz): {len(matriz)} | {n_col_nuevo > len(matriz[0])}')
    actualizar = False
    if n_col_nuevo > len(matriz[0]): # Agrego columna
        for fila in matriz:
            fila.append(0.0)
        headers_columnas.append(f'Columna {columnas_spinbox.get()}')
        actualizar = True
    elif n_col_nuevo < len(matriz[0]): # Elimino columna
        matriz = [fila[:-1] for fila in matriz]
        headers_columnas = headers_columnas[:-1]
        actualizar = True
    if actualizar:
        sheet.destroy()
        sheet = DoubleEntryTable(frame_datos, matriz, headers_columnas, headers_filas, read_str_and_replace_header)
        sheet.grid(column=0, row=0)

def handle_row_spinbox():
    global filas_spinbox
    global matriz
    global headers_filas
    global sheet
    n_filas_nuevo = int(filas_spinbox.get())
    actualizar = False
    if n_filas_nuevo > len(matriz): # Agrego columna
        matriz.append([0.0 for _ in range(len(matriz[0]))])
        headers_filas.append(f'Fila {filas_spinbox.get()}')
        actualizar = True
    elif n_filas_nuevo < len(matriz): # Elimino columna
        matriz = matriz[:-1]
        headers_filas = headers_filas[:-1]
        actualizar = True
    if actualizar:
        sheet.destroy()
        sheet = DoubleEntryTable(frame_datos, matriz, headers_columnas, headers_filas, read_str_and_replace_header)
        sheet.grid(column=0, row=0)

columnas_frame = tk.LabelFrame(sheet_config_frame, text='Columnas', borderwidth=0)
columnas_spinbox = tk.Spinbox(columnas_frame, values=[i for i in range(2, 11)], command=handle_col_spinbox)
columnas_spinbox.delete(0, tk.END)
columnas_spinbox.insert(0, 4)
columnas_spinbox.pack()
columnas_frame.grid(column=1, row=0)

filas_frame = tk.LabelFrame(sheet_config_frame, text='Filas', borderwidth=0)
filas_spinbox = tk.Spinbox(filas_frame, values=[i for i in range(2, 11)], command=handle_row_spinbox)
filas_spinbox.delete(0, tk.END)
filas_spinbox.insert(0, 4)
filas_spinbox.pack()
filas_frame.grid(column=1, row=1)

btn_calcular = tk.Button(sheet_config_frame, text='Calcular')
btn_calcular.bind('<Button-1>', lambda e: regenerar_analisis(sheet, frame_analisis))
btn_calcular.grid(column=1, row=2)

sheet_config_frame.grid(column=1, row=0)

## Criterios

frame_analisis = tk.Frame(frame_principal, padx=5, pady=5)
frame_analisis.grid(column=0, row=2, sticky=tk.NSEW)

wald_frame = Wald(frame_analisis, sheet.get_values_as_list(), sheet.get_row_headers())
wald_frame.grid(column=0, row=0, sticky=tk.NSEW)

maximax_frame = Maximax(frame_analisis, sheet.get_values_as_list(), sheet.get_row_headers())
maximax_frame.grid(column=1, row=0, sticky=tk.NSEW)

frame_hurwicz = Hurwicz(frame_analisis, sheet.get_values_as_list(), sheet.get_row_headers())
frame_hurwicz.grid(column=0, row=1, sticky=tk.NSEW)

frame_savage = Savage(frame_analisis, sheet.get_values_as_list(), sheet.get_row_headers(), sheet.get_column_headers())
frame_savage.grid(column=1, row=1, sticky=tk.NSEW)

frame_esperanza = Esperanza(frame_analisis, sheet.get_values_as_list(), sheet.get_row_headers(), sheet.get_column_headers())
frame_esperanza.grid(column=0, row=2, columnspan=2)

frame_principal.pack()

window.mainloop()

