import tkinter as tk
import tkinter.simpledialog
from tkinter.ttk import Notebook, Combobox, Style

window = tk.Tk()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_POS_X = window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2
WINDOW_POS_Y = window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2


window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.title('Analizador')

nb = Notebook(window)

frame_datos = tk.Frame(nb)

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

def leer_string_y_reemplazar(event):
    nuevo_texto = tk.simpledialog.askstring('Ingrese nuevo texto', 'Nuevo texto')
    event.widget['text'] = nuevo_texto

def agregar_columna(event):
    print(event.widget)
    pass

def agregar_fila(event):
    print(event.widget)
    pass

n = 4

for row in range(n):
    label_letra = tk.Label(frame_datos, text=chr(ord('A') + row), width=5)
    label_letra.grid(column=2 + row, row=0, padx=0, pady=0)
    label_letra.bind('<Button-1>', leer_string_y_reemplazar)
    label_number = tk.Label(frame_datos, text=chr(ord('1') + row), width=5)
    label_number.grid(column=1, row=1 + row, padx=0, pady=0)
    label_number.bind('<Button-1>', leer_string_y_reemplazar)
    for column in range(0, n):
        t = tk.Entry(frame_datos, width=10)
        #t = tk.Label(f, width=5, background='#ffffff', border=1, borderwidth=1)
        t.grid(column=column + 2, row=row + 1, pady=0)

btn_agregar_columna = tk.Button(frame_datos, text='+', width=2)
btn_agregar_columna.grid(column=n + 2, row=0, padx=10)
btn_agregar_columna.bind('<Button-1>', agregar_columna)
btn_agregar_fila = tk.Button(frame_datos, text='+', width=2)
btn_agregar_fila.grid(column=1, row=n + 1)
btn_agregar_fila.bind('<Button-1>', agregar_fila)


nb.add(frame_datos, text='Ingreso de datos')
nb.add(tk.Label(nb, text='label 2'), text='Análisis')

nb.pack(fill='both')

window.mainloop()

