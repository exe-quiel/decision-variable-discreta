import random

def cargar_matriz_random(n_filas, n_columnas, n_min, n_max):
    matriz = cargar_matriz_valor(n_filas, n_columnas)
    for y in range(n_filas):
        for x in range(n_columnas):
            matriz[y][x] = random.uniform(n_min, n_max)
    return matriz

def cargar_matriz_valor(n_filas, n_columnas, valor=0):
    matriz = []
    for indice_fila in range(n_filas):
        fila = []
        for indice_columna in range(n_columnas):
            fila.append(valor)
        matriz.append(fila)
    return matriz

def cargar_matriz_ejercicio():
    n_filas = 4
    n_columnas = 4
    matriz = cargar_matriz_valor(n_filas, n_columnas)
    
    # Acción: Compro grande
    matriz[0][0] =  2.5 # Estado natural: muy buenas
    matriz[0][1] =  0.0 # Estado natural: buenas
    matriz[0][2] = -2.5 # Estado natural: regulares
    matriz[0][3] = -4.1 # Estado natural: malas
    # Acción: Compro mediana
    matriz[1][0] =  1.6 # Estado natural: muy buenas
    matriz[1][1] =  0.3 # Estado natural: buenas
    matriz[1][2] = -1.2 # Estado natural: regulares
    matriz[1][3] = -2.1 # Estado natural: malas
    # Acción: Compro chica
    matriz[2][0] =  0.6 # Estado natural: muy buenas
    matriz[2][1] =  0.4 # Estado natural: buenas
    matriz[2][2] = -0.3 # Estado natural: regulares
    matriz[2][3] = -0.3 # Estado natural: malas
    # Acción: No compro nada
    matriz[3][0] = -0.4 # Estado natural: muy buenas
    matriz[3][1] =  0.0 # Estado natural: buenas
    matriz[3][2] =  0.0 # Estado natural: regulares
    matriz[3][3] =  0.0 # Estado natural: malas

    return matriz, n_filas, n_columnas

def calcular_valores_min_fila(matriz):
    '''
    Recibe una matriz y devuelve una lista que contiene los valores mínimos de cada fila
    '''
    #return [min(matriz[i]) for i in len(matriz)]
    menores = []
    for i in range(len(matriz)):
        menores.append(min(matriz[i]))
    return menores

def calcular_valores_max_fila(matriz):
    '''
    Recibe una matriz y devuelve una lista que contiene los valores máximos de cada fila
    '''
    #return [max(matriz[i]) for i in len(matriz)]
    mayores = []
    for i in range(len(matriz)):
        mayores.append(max(matriz[i]))
    return mayores

def calcular_valores_max_columna(matriz):
    '''
    Recibe una matriz y devuelve una lista que contiene los valores máximos de cada columna
    '''
    mayores = []
    for i in range(len(matriz[0])):
        valores_columna = [fila[i] for fila in matriz]
        mayores.append(max(valores_columna))
    return mayores


## CRITERIOS PARA INCERTIDUMBRE (CUANDO NO CONOZCO LAS PROBABILIDADES)

## 1. Criterio de Wald (pesimista, maximin) -> max(min(bij))

def calcular_maximin(matriz):
    '''
    Recibe una matriz, obtiene los valores mínimos de cada fila y devuelve el máximo de esos valores
    '''
    valores_min = calcular_valores_min_fila(matriz)
    mayor = valores_min[0]
    #y_mayores = [0]
    y_mayores = []
    for y in range(len(valores_min)):
        if valores_min[y] > mayor:
            mayor = valores_min[y]
            y_mayores.clear()
            y_mayores.append(y)
        elif valores_min[y] == mayor:
            y_mayores.append(y)

    celdas_mayores = []
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] == mayor:
                celdas_mayores.append((x, y))

    # valores mínimos de cada fila, valor maximin, filas con el valor maximin, celdas de la matriz original con el valor maximin
    return valores_min, mayor, y_mayores, celdas_mayores

## 2. Criterio optimista (maximax)

def calcular_maximax(matriz):
    '''
    Recibe una matriz, obtiene los valores máximos de cada fila y devuelve el máximo de esos valores
    '''
    valores_max = calcular_valores_max_fila(matriz)
    mayor = valores_max[0]
    #y_mayores = []
    y_mayores = []
    for y in range(len(valores_max)):
        if valores_max[y] > mayor:
            mayor = valores_max[y]
            y_mayores.clear()
            y_mayores.append(y)
        elif valores_max[y] == mayor:
            y_mayores.append(y)

    celdas_mayores = []
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] == mayor:
                celdas_mayores.append((x, y))

    # valores máximos de cada fila, valor maximax, filas con el valor maximax, celdas de la matriz original con el valor maximax
    return valores_max, mayor, y_mayores, celdas_mayores

## 3. Criterio de Hurwicz

def calcular_valores_hurwicz(matriz, coef_optim):
    valores_max = calcular_valores_max_fila(matriz)
    valores_min = calcular_valores_min_fila(matriz)
    #return [coef_optim * valores_max[i] + (1 - coef_optim) * valores_min[i] for i in len(matriz)]
    valores_hurwicz = []
    for i in range(len(matriz)):
        valores_hurwicz.append(coef_optim * valores_max[i] + (1 - coef_optim) * valores_min[i])
    return valores_hurwicz

def calcular_hurwicz(matriz, coef_optim):
    valores_hurwicz = calcular_valores_hurwicz(matriz, coef_optim)
    mayor = valores_hurwicz[0]
    #y_mayores = [0]
    y_mayores = []
    for i in range(len(valores_hurwicz)):
        if valores_hurwicz[i] > mayor:
            mayor = valores_hurwicz[i]
            y_mayores.clear()
            y_mayores.append(i)
        elif valores_hurwicz[i] == mayor:
            y_mayores.append(i)

     # columna de valores, valor mayor, filas que contienen el mayor
    return valores_hurwicz, mayor, y_mayores

## 4. Criterio de Savage (arrepentimiento, minimax)

def construir_matriz_arrepentimiento(matriz):
    # Por cada estado (columna) de la matriz original,
    # calculo el arrepentimiento para cada acción (fila)
    # si se da ese estado
    matriz_arrepentimiento = cargar_matriz_valor(len(matriz), len(matriz[0]))
    for indice_columna in range(len(matriz[0])):
        valores_columna = []
        for fila in matriz:
            valores_columna.append(fila[indice_columna])
        valor_maximo_columna = max(valores_columna)
        for indice_fila in range(len(valores_columna)):
            valor_beneficio = valores_columna[indice_fila]
            valor_arrepentimiento = valor_maximo_columna - valor_beneficio
            matriz_arrepentimiento[indice_fila][indice_columna] = valor_arrepentimiento
    return matriz_arrepentimiento

def calcular_savage(matriz):
    matriz_arrepentimiento = construir_matriz_arrepentimiento(matriz)
    valores_max_fila = calcular_valores_max_fila(matriz_arrepentimiento)

    menor = valores_max_fila[0]
    #y_menores = [0]
    y_menores = []
    for y in range(len(valores_max_fila)):
        if valores_max_fila[y] < menor:
            menor = valores_max_fila[y]
            y_menores.clear()
            y_menores.append(y)
        elif valores_max_fila[y] == menor:
            y_menores.append(y)

    celdas_menores = []
    for y in range(len(matriz_arrepentimiento)):
        for x in range(len(matriz_arrepentimiento[y])):
            if matriz_arrepentimiento[y][x] == menor:
                celdas_menores.append((x, y))

    # matriz de arrepentimiento
    # valores máximos de cada fila (matriz de arrepentimiento)
    # valor minimax
    # filas con el valor minimax (matriz de arrepentimiento)
    # celdas de la matriz de arrepentimiento con el valor minimax
    return matriz_arrepentimiento, valores_max_fila, menor, y_menores, celdas_menores

## CRITERIOS PARA RIESGO (CONOZCO LAS PROBABILIDADES, P(x) < 1, SUMATORIA P(x) = 1)

## 5. Máximo beneficio esperado

def calcular_max_beneficio_esperado(matriz, vector_probabilidades=[], usar_laplace=False):
    if usar_laplace:
        vector_probabilidades = [1/len(matriz[0]) for _ in range(len(matriz))]
        print(vector_probabilidades)

    vector_esperanzas = []
    for fila in matriz:
        esperanza = 0
        for indice_columna in range(len(fila)):
            esperanza += vector_probabilidades[indice_columna] * fila[indice_columna]
        vector_esperanzas.append(esperanza)

    mayor = vector_esperanzas[0]
    #y_mayores = [0]
    y_mayores = []
    for i in range(len(vector_esperanzas)):
        if vector_esperanzas[i] > mayor:
            mayor = vector_esperanzas[i]
            y_mayores.clear()
            y_mayores.append(i)
        elif vector_esperanzas[i] == mayor:
            y_mayores.append(i)
    return vector_esperanzas, mayor, y_mayores

## 6. Beneficio esperado con información perfecta (BEIP)

def calcular_beip(matriz, vector_probabilidades=[], usar_laplace=False):
    if usar_laplace:
        vector_probabilidades = [1/len(matriz[0]) for _ in range(len(matriz))]
        print(vector_probabilidades)

    valores_max_columna = calcular_valores_max_columna(matriz)

    beip = 0
    for indice_columna in range(len(valores_max_columna)):
        beip += vector_probabilidades[indice_columna] * valores_max_columna[indice_columna]

    return beip

## 7. Valor esperado con información perfecta (VEIP)
def calcular_veip(matriz, vector_probabilidades=[], usar_laplace=False):
    beip = calcular_beip(matriz, vector_probabilidades, usar_laplace)
    _, max_esperanza, _ = calcular_max_beneficio_esperado(matriz, vector_probabilidades, usar_laplace)
    return beip - max_esperanza

## Main

if __name__ == '__main__':
    matriz, _, _ = cargar_matriz_ejercicio()
    #matriz = cargar_matriz_random(5, 5, -4, 4)
    print(matriz)
    #print("Wald: " + str(calcular_maximax(matriz)))
    #print(calcular_maximin(matriz))
    #print(calcular_hurwicz(matriz, 0.4))
    #print(calcular_savage(matriz))
    #print(calcular_max_beneficio_esperado(matriz, [0.2, 0.2, 0.4, 0.2]))
    #print(calcular_beip(matriz, [0.2, 0.2, 0.4, 0.2]))
    print(calcular_veip(matriz, [0.2, 0.2, 0.4, 0.2]))
    
