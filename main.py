import tkinter as tk
import tkinter.simpledialog
from tkinter.ttk import Notebook, Combobox, Style, Separator
from table import DoubleEntryTable

from utils import *

window = tk.Tk()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650
WINDOW_POS_X = window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2
WINDOW_POS_Y = window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2


window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.title('Analizador')

frame_principal = tk.Frame(window)

frame_datos = tk.LabelFrame(frame_principal, width=5, text='Datos', padx=5, pady=5)
frame_datos.grid(column=0, row=0, sticky=tk.NSEW)
#vscrollbar = tk.Scrollbar(frame_datos, orient='vertical')
#vscrollbar.grid(column=10, row=0, rowspan=10)
#vscrollbar.pack(side='right', fill='y')



#separator = Separator(frame_principal, orient='horizontal')
#separator.grid(column=0, row=1, sticky='WE', pady=5)

frame_analisis = tk.Frame(frame_principal, padx=5, pady=5)
frame_analisis.grid(column=0, row=2, sticky=tk.NSEW)

#nb = Notebook(frame_analisis)

'''
label_frame = tk.LabelFrame(frame_analisis, text="TEXT")
label_frame.grid(column=0, row=0, rowspan=10)
entry = tk.Entry(label_frame)
entry.pack()
'''

'''
style = Style()
style.theme_settings("default", {
   "TCombobox": {
       #"configure": {"padding": 10},
       "map": {
           "background": [("active", "green2"),
                          ("!disabled", "green4")],
           "fieldbackground": [("!disabled", "green3")],
           "foreground": [("focus", "OliveDrab1"),
                          ("!disabled", "OliveDrab2")]
       }
   }
})
'''

#combo = Combobox(window, values=['Wald (maximax)', 'Optimista (maximin)', 'Hurwicz', 'Savage (minimax)', 'Máximo beneficio esperado'])
#combo.pack()

matriz, _, _ = cargar_matriz_ejercicio()
headers_columnas = ['Muy bueno', 'Bueno', 'Regular', 'Malo']
headers_filas = ['Grande', 'Mediana', 'Chica', 'Nada']

#matriz = cargar_matriz_random(3, 5, -20, 20)
#headers_columnas = ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5']
#headers_filas = ['Fila 1', 'Fila 2', 'Fila 3']

def read_str_and_replace_header(event):
    new_text = tk.simpledialog.askstring('New header text', 'Type new text')
    event.widget['text'] = new_text

sheet = DoubleEntryTable(frame_datos, matriz, headers_columnas, headers_filas, read_str_and_replace_header)
sheet.grid(column=0, row=0)

sheet_config_frame = tk.Frame(frame_datos)

columnas_frame = tk.LabelFrame(sheet_config_frame, text='Columnas', borderwidth=0)
columnas_spinbox = tk.Spinbox(columnas_frame, values=[i for i in range(2, 11)])
columnas_spinbox.pack()
columnas_frame.grid(column=0, row=0)

filas_frame = tk.LabelFrame(sheet_config_frame, text='Filas', borderwidth=0)
filas_spinbox = tk.Spinbox(filas_frame, values=[i for i in range(2, 11)])
filas_spinbox.pack()
filas_frame.grid(column=0, row=1)

btn_calcular = tk.Button(sheet_config_frame, text='Calcular')
btn_calcular.bind('<Button-1>', lambda e: print(e))
btn_calcular.grid(column=0, row=2)

sheet_config_frame.grid(column=1, row=0)

frame_wald = tk.LabelFrame(frame_analisis, text='Wald', padx=5, pady=5)
valores_min, mayor, y_mayores, celdas_mayores = calcular_maximin(matriz)

wald_table = DoubleEntryTable(frame_wald, [valores_min], headers_filas, ['Mínimos por fila'], disable_values=True)
print(valores_min, mayor, y_mayores, celdas_mayores)
wald_resultado = tk.Label(frame_wald, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})')
wald_resultado.pack()

frame_wald.grid(column=0, row=0, sticky=tk.NSEW)

#nb.add(frame_wald, text='Wald (pesimista)')

frame_maximax = tk.LabelFrame(frame_analisis, text='Optimista', padx=5, pady=5)
valores_max, mayor, y_mayores, celdas_mayores = calcular_maximax(matriz)

maximax_table = DoubleEntryTable(frame_maximax, [valores_max], headers_filas, ['Máximos por fila'], disable_values=True)
print(valores_max, mayor, y_mayores, celdas_mayores)
maximax_resultado = tk.Label(frame_maximax, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})')
maximax_resultado.pack()

frame_maximax.grid(column=1, row=0, sticky=tk.NSEW)

#nb.add(frame_maximax, text='Optimista')

frame_hurwicz = tk.LabelFrame(frame_analisis, text='Hurwicz', padx=5, pady=5)

coeficiente_opt_frame = tk.LabelFrame(frame_hurwicz, text='Coeficiente de optimismo', borderwidth=0)
coef_entry = tk.Entry(coeficiente_opt_frame)
coef_entry.pack(fill=tk.X, expand=tk.FALSE)
coeficiente_opt_frame.pack(fill=tk.BOTH, expand=tk.TRUE)

valores_hurwicz, mayor, y_mayores = calcular_hurwicz(matriz, 0.4)
print(valores_hurwicz, mayor, y_mayores)

hurwicz_table = DoubleEntryTable(frame_hurwicz, [valores_hurwicz], headers_filas, ['Valor por fila'], disable_values=True)
hurwicz_resultado = tk.Label(frame_hurwicz, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})')
hurwicz_resultado.pack()

frame_hurwicz.grid(column=0, row=1, sticky=tk.NSEW)

#nb.add(frame_hurwicz, text='Hurwicz')

frame_savage = tk.LabelFrame(frame_analisis, text='Savage', padx=5, pady=5)

matriz_arrepentimiento, valores_savage, menor, y_menores, celdas_menores = calcular_savage(matriz)
print(valores_savage, menor, y_menores, celdas_menores)

savage_table_regret = DoubleEntryTable(frame_savage, matriz_arrepentimiento, headers_columnas, headers_filas, disable_values=True)
savage_table = DoubleEntryTable(frame_savage, [valores_savage], headers_filas, ['Valor por fila'], disable_values=True)
savage_resultado = tk.Label(frame_savage, text=f'Mejor opción: {headers_filas[y_menores[0]]} ({menor})')
savage_resultado.pack()

frame_savage.grid(column=1, row=1, sticky=tk.NSEW)

#nb.add(frame_savage, text='Savage')

frame_esperanza = tk.LabelFrame(frame_analisis, text='Esperanza', padx=5, pady=5)

vector_esperanzas, mayor, y_mayores = calcular_max_beneficio_esperado(matriz, [0.2, 0.2, 0.4, 0.2])
print(vector_esperanzas, mayor, y_mayores)

beip = calcular_beip(matriz, [0.2, 0.2, 0.4, 0.2])
veip = calcular_veip(matriz, [0.2, 0.2, 0.4, 0.2])

max_esperanza_table = DoubleEntryTable(frame_esperanza, [vector_esperanzas], headers_filas, ['Máxima esperanza por fila'], disable_values=True)
max_esperanza_resultado = tk.Label(frame_esperanza, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})')
max_esperanza_resultado.pack()

beip_resultado = tk.Label(frame_esperanza, text=f'BEIP: {beip}')
beip_resultado.pack()

veip_resultado = tk.Label(frame_esperanza, text=f'VEIP: {veip}')
veip_resultado.pack()

frame_esperanza.grid(column=0, row=2, columnspan=2, sticky=tk.NSEW)

#nb.add(frame_esperanza, text='Esperanza')

#nb.pack(fill=tk.BOTH, expand=tk.TRUE)

frame_principal.pack()

window.mainloop()

