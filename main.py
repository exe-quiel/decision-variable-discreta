import tkinter as tk
from tkinter.ttk import Notebook, Combobox, Style

window = tk.Tk()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_POS_X = window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2
WINDOW_POS_Y = window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2


window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.title('Analizador')

nb = Notebook(window)

frame_analisis = tk.Frame(nb)

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

n = 5

for row in range(n):
    label_letra = tk.Label(frame_analisis, text=chr(ord('A') + row))
    label_letra.grid(column=2 + row, row=0)
    label_number = tk.Label(frame_analisis, text=chr(ord('1') + row))
    label_number.grid(column=1, row=1 + row)
    for column in range(0, n):
        t = tk.Entry(frame_analisis, width=5)
        #t = tk.Label(f, width=5, background='#ffffff', border=1, borderwidth=1)
        t.grid(column=column + 2, row=row + 1)

nb.add(frame_analisis, text='Ingreso de datos')
nb.add(tk.Label(nb, text='label 2'), text='Análisis')

nb.pack(fill='both')

window.mainloop()

