import tkinter as tk

from utils import *
from table import DoubleEntryTable



class Wald(tk.LabelFrame):

    def __init__(self, parent, matriz, headers_filas, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, text='Wald', padx=5, pady=5, *args, **kwargs)
        valores_min, mayor, y_mayores, celdas_mayores = calcular_maximin(matriz)

        DoubleEntryTable(self, [valores_min], headers_filas, ['Mínimos'], disable_values=True)
        tk.Label(self, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})').pack()


class Maximax(tk.LabelFrame):

    def __init__(self, parent, matriz, headers_filas, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, text='Optimista', padx=5, pady=5, *args, **kwargs)
        valores_max, mayor, y_mayores, celdas_mayores = calcular_maximax(matriz)

        DoubleEntryTable(self, [valores_max], headers_filas, ['Máximos'], disable_values=True)
        tk.Label(self, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})').pack()


class Hurwicz(tk.LabelFrame):

    def __init__(self, parent, matriz, headers_filas, coeficiente=0.5, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, text='Hurwicz', padx=5, pady=5, *args, **kwargs)
        coeficiente_opt_frame = tk.LabelFrame(self, text='Coeficiente de optimismo', borderwidth=0)
        self.coef_entry = tk.Entry(coeficiente_opt_frame)
        self.coef_entry.delete(0, tk.END)
        self.coef_entry.insert(0, coeficiente)
        self.coef_entry.pack(fill=tk.X, expand=tk.FALSE)
        coeficiente_opt_frame.pack(fill=tk.BOTH, expand=tk.TRUE)

        valores_hurwicz, mayor, y_mayores = calcular_hurwicz(matriz, coeficiente)

        DoubleEntryTable(self, [valores_hurwicz], headers_filas, ['Valor'], disable_values=True)
        tk.Label(self, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})').pack()

    def get_coeficiente(self):
        return float(self.coef_entry.get())


class Savage(tk.LabelFrame):

    def __init__(self, parent, matriz, headers_filas, headers_columnas, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, text='Savage', padx=5, pady=5, *args, **kwargs)
        matriz_arrepentimiento, valores_savage, menor, y_menores, celdas_menores = calcular_savage(matriz)

        DoubleEntryTable(self, matriz_arrepentimiento, headers_columnas, headers_filas, disable_values=True)
        DoubleEntryTable(self, [valores_savage], headers_filas, ['Valor'], disable_values=True)
        tk.Label(self, text=f'Mejor opción: {headers_filas[y_menores[0]]} ({menor})').pack()


class Esperanza(tk.LabelFrame):

    def __init__(self, parent, matriz, headers_filas, headers_columnas, probabilidades=None, usar_laplace=True, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, text='Esperanza', padx=5, pady=5, *args, **kwargs)

        if not probabilidades or usar_laplace:
            # Distribuye las probabilidades de los estados de forma equitativa
            probabilidades = [1/len(matriz[0]) for _ in matriz[0]]

        vector_esperanzas, mayor, y_mayores = calcular_max_beneficio_esperado(matriz, probabilidades)
        beip = calcular_beip(matriz, probabilidades)
        veip = calcular_veip(matriz, probabilidades)

        prob_frame = tk.Frame(self)

        self.usar_laplace_var = tk.BooleanVar(prob_frame, value=usar_laplace)
        self.btn_usar_laplace = tk.Checkbutton(prob_frame, text='Usar Laplace', variable=self.usar_laplace_var)
        self.btn_usar_laplace.grid(column=0, row=0)

        self.probabilidades_entries = []

        for indice, header in enumerate(headers_columnas):
            lf = tk.LabelFrame(prob_frame, text=header)
            prob_entry = tk.Entry(lf)
            prob_entry.delete(0, tk.END)
            prob_entry.insert(0, probabilidades[indice])
            prob_entry.pack()
            lf.grid(column=indice + 1, row=0)
            self.probabilidades_entries.append(prob_entry)

        prob_frame.pack()

        max_esperanza_table = DoubleEntryTable(self, [vector_esperanzas], headers_filas, ['Máx. esp.'], disable_values=True)

        max_esperanza_resultado = tk.Label(self, text=f'Mejor opción: {headers_filas[y_mayores[0]]} ({mayor})')
        max_esperanza_resultado.pack()

        beip_resultado = tk.Label(self, text=f'BEIP: {beip}')
        beip_resultado.pack()

        veip_resultado = tk.Label(self, text=f'VEIP: {veip}')
        veip_resultado.pack()

    def get_probabilidades(self):    
        return [float(prob_entry.get()) for prob_entry in self.probabilidades_entries]

    def is_usar_laplace(self):
        return self.usar_laplace_var.get()
