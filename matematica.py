PI = 3.141592653589793
E  = 2.718281828459045

# BASICAS

def valor_absoluto(x):
    return x if x >= 0 else -x


def potencia(base, exp):
    if exp == 0:
        return 1.0

    negativo = exp < 0
    exp = int(valor_absoluto(exp))

    resultado = 1.0
    for _ in range(exp):
        resultado *= base

    return 1.0 / resultado if negativo else resultado

# FACTORIAL (para series)

def factorial(n):
    if n < 0:
        raise ValueError("Factorial no definido para negativos")
    resultado = 1
    for i in range(1, int(n) + 1):
        resultado *= i
    return resultado

# RAICES (Newton)

def raiz(x, n=2):
    if n <= 0:
        raise ValueError("Indice de raiz invalido")

    if x < 0 and n % 2 == 0:
        raise ValueError("Raiz par de numero negativo no definida")

    if x == 0:
        return 0.0

    estimado = x / n

    for _ in range(50):
        estimado = ((n - 1) * estimado + x / potencia(estimado, n - 1)) / n

    return estimado

# EXPONENCIAL (serie)

def exponencial(x):
    suma = 1.0
    termino = 1.0

    for n in range(1, 50):
        termino *= x / n
        suma += termino

        if valor_absoluto(termino) < 1e-12:
            break

    return suma

# LOG NATURAL (aprox)

def logaritmo_natural(x):
    if x <= 0:
        raise ValueError("ln(x) no definido para x <= 0")

    y = (x - 1) / (x + 1)
    y2 = y * y

    suma = 0.0
    termino = y

    for n in range(1, 50, 2):
        suma += termino / n
        termino *= y2

    return 2 * suma

# NORMALIZAR ANGULO

def _normalizar(x):
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    return x

# TRIGONOMETRIA (series)

def seno(x):
    x = _normalizar(x)

    suma = 0.0
    termino = x

    for n in range(1, 20):
        suma += termino
        termino *= -x * x / ((2 * n) * (2 * n + 1))

    return suma


def coseno(x):
    x = _normalizar(x)

    suma = 0.0
    termino = 1.0

    for n in range(1, 20):
        suma += termino
        termino *= -x * x / ((2 * n - 1) * (2 * n))

    return suma


def tangente(x):
    c = coseno(x)

    if valor_absoluto(c) < 1e-10:
        raise ValueError("tan(x) indefinida")

    return seno(x) / c

# REGRESION LINEAL

def regresion_lineal(X, Y):

    if len(X) == 0:
        raise ValueError("Datos vacios")

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

    if len(modelo) != 2:
        raise ValueError("Modelo invalido")

    m, b = modelo
    return m * x + b

# ERROR MSE

def mse(X, Y, modelo):

    if len(X) == 0:
        raise ValueError("Datos vacios")

    if isinstance(X[0], list):
        X = [fila[0] for fila in X]

    if isinstance(Y[0], list):
        Y = [fila[0] for fila in Y]

    if len(X) != len(Y):
        raise ValueError("X y Y deben tener el mismo tamaño")

    m, b = modelo
    n = len(X)

    error = 0.0

    for i in range(n):
        pred = m * X[i] + b
        error += (Y[i] - pred) ** 2

    return error / n
