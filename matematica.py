def valor_absoluto(x):
    return x if x >= 0 else -x


def potencia(base, exp):
    return base ** exp


def raiz(x, n=2):
    return x ** (1.0 / n)


def exponencial(x):
    return 2.718281828459045 ** x


def logaritmo_natural(x):
    import math
    return math.log(x)


def seno(x):
    import math
    return math.sin(x)


def coseno(x):
    import math
    return math.cos(x)


def tangente(x):
    import math
    return math.tan(x)


# REGRESION LINEAL

def regresion_lineal(X, Y):

    if isinstance(X[0], list):
        X = [fila[0] for fila in X]

    if isinstance(Y[0], list):
        Y = [fila[0] for fila in Y]

    if len(X) != len(Y):
        raise ValueError("X y Y deben tener el mismo tamaño")

    n = len(X)

    sum_x = sum(X)
    sum_y = sum(Y)

    sum_xy = 0.0
    sum_x2 = 0.0

    for i in range(n):
        sum_xy += X[i] * Y[i]
        sum_x2 += X[i] * X[i]

    denom = n * sum_x2 - sum_x * sum_x

    if denom == 0:
        raise ValueError("Division por cero en regresion")

    m = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y - m * sum_x) / n

    return [m, b]

# PREDICCION

def predecir(modelo, x):
    m, b = modelo
    return m * x + b

# ERROR

def mse(X, Y, modelo):

    if isinstance(X[0], list):
        X = [fila[0] for fila in X]

    if isinstance(Y[0], list):
        Y = [fila[0] for fila in Y]

    m, b = modelo
    n = len(X)

    error = 0.0

    for i in range(n):
        pred = m * X[i] + b
        error += (Y[i] - pred) ** 2

    return error / n
