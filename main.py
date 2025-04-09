import tkinter as tk
from tkinter.ttk import Notebook

window = tk.Tk()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_POS_X = window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2
WINDOW_POS_Y = window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2


window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POS_X}+{WINDOW_POS_Y}')
window.title('Analizador')

frame = tk.Frame(window)

nb = Notebook(frame)
nb2_frame = tk.Frame(nb)
lbl = tk.Label(nb2_frame, text='label 2')
nb.add(tk.Label(nb2_frame, text='label 1'), text='NB1')
nb.add(tk.Label(nb, text='label 1'), text='NB1')
nb.add(nb2_frame, text='NB2')

nb.pack()
frame.pack()

window.mainloop()