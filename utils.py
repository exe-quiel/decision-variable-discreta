import random

def cargar_matriz_random(n_filas, n_columnas, n_min, n_max):
    matriz = [[]]
    for y in range(n_filas):
        for x in range(n_columnas):
            matriz[y][x] = random.uniform(n_min, n_max)
    return matriz

def cargar_matriz_ejercicio():
    n_filas = 4
    n_columnas = 4
    matriz = [[]]
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

def calcular_valores_min(matriz):
    #return [min(matriz[i]) for i in len(matriz)]
    menores = []
    for i in len(matriz):
        menores[i] = min(matriz[i])
    return menores

def calcular_valores_max(matriz):
    #return [max(matriz[i]) for i in len(matriz)]
    mayores = []
    for i in len(matriz):
        mayores[i] = max(matriz[i])
    return mayores


## CRITERIOS PARA INCERTIDUMBRE (NO CONOZCO LAS PROBABILIDADES)

## 1. Criterio de Wald (pesimista, maximin) -> max(min(bij))

def calcular_maximin(matriz):
    valores_min = calcular_valores_min(matriz)
    mayor = valores_min[0]
    y_mayores = [0]
    for y in len(valores_min):
        if valores_min[0] > mayor:
            mayor = valores_min[0]
            y_mayores.clear()
            y_mayores.append(y)
        elif valores_min[0] == mayor:
            y_mayores.append(y)

    celdas_mayores = []
    for y in len(matriz):
        for x in len(matriz[y]):
            if matriz[y][x] == mayor:
                celdas_mayores.append((x, y))

    # valores mínimos de cada fila, valor maximin, filas con el valor maximin, celdas de la matriz original con el valor maximin
    return valores_min, mayor, y_mayores, celdas_mayores

## 2. Criterio optimista (maximax)

def calcular_maximax(matriz):
    valores_max = calcular_valores_max(matriz)
    mayor = valores_max[0]
    y_mayores = [0]
    for y in len(valores_max):
        if valores_max[0] > mayor:
            mayor = valores_max[0]
            y_mayores.clear()
            y_mayores.append(y)
        elif valores_max[0] == mayor:
            y_mayores.append(y)

    celdas_mayores = []
    for y in len(matriz):
        for x in len(matriz[y]):
            if matriz[y][x] == mayor:
                celdas_mayores.append((x, y))

    # valores máximos de cada fila, valor maximax, filas con el valor maximax, celdas de la matriz original con el valor maximax
    return valores_max, mayor, y_mayores, celdas_mayores

## 3. Criterio de Hurwicz

coeficiente_optimismo = 0.5

def calcular_valores_hurwicz(matriz, coef_optim):
    valores_max = calcular_valores_max(matriz)
    valores_min = calcular_valores_min(matriz)
    #return [coef_optim * valores_max[i] + (1 - coef_optim) * valores_min[i] for i in len(matriz)]
    valores_hurwicz = []
    for i in len(matriz):
        valores_hurwicz[i] = coef_optim * valores_max[i] + (1 - coef_optim) * valores_min[i]
    return valores_hurwicz

def calcular_hurwicz(matriz, coef_optim):
    valores_hurwicz = calcular_valores_hurwicz(matriz, coef_optim)
    mayor = valores_hurwicz[0]
    y_mayores = [0]
    for i in len(valores_hurwicz)[1:]:
        if valores_hurwicz[i] > mayor:
            mayor = valores_hurwicz[i]
            y_mayores.clear()
            y_mayores.append(i)
        elif valores_hurwicz[i] == mayor:
            y_mayores.append(i)

     # columna de valores, valor mayor, filas que contienen el mayor
    return valores_hurwicz, mayor, y_mayores

## 4. Criterio de Savage (arrepentimiento, minimax)

## CRITERIOS PARA RIESGO (CONOZCO LAS PROBABILIDADES, P(x) < 1, SUMATORIA P(x) = 1)

## 5. Máximo beneficio esperado

## 6. Beneficio esperado con información perfecta (BEIP)

## 7. Valor esperado con información perfecta (VEIP)



