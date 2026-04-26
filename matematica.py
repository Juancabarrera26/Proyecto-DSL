PI = 3.141592653589793
E  = 2.718281828459045

# OPERACIONES BASICAS

def valor_absoluto(x):
    return x if x >= 0 else -x


def potencia(base, exp):
    if exp == 0:
        return 1.0

    if isinstance(exp, float) and not exp.is_integer():
        return exponencial(exp * logaritmo_natural(base))

    n = int(exp)
    negativo = n < 0
    n = abs(n)

    resultado = 1.0
    for _ in range(n):
        resultado *= base

    return 1.0 / resultado if negativo else resultado

# RAICES

def raiz(x, n=2):
    if x < 0 and n % 2 == 0:
        raise ValueError("Raiz par de numero negativo no definida")

    if x == 0:
        return 0.0

    estimado = x / n

    for _ in range(100):
        estimado = ((n - 1) * estimado + x / potencia(estimado, n - 1)) / n

    return estimado

# EXPONENCIAL Y LOG

def exponencial(x):
    suma = 1.0
    termino = 1.0

    for n in range(1, 100):
        termino *= x / n
        suma += termino

        if valor_absoluto(termino) < 1e-15:
            break

    return suma


def logaritmo_natural(x):
    if x <= 0:
        raise ValueError("ln(x) no definido para x <= 0")

    k = 0

    while x > 2:
        x /= 2
        k += 1

    while x < 0.5:
        x *= 2
        k -= 1

    y = (x - 1) / (x + 1)
    y2 = y * y

    suma = 0.0
    potencia_y = y

    for n in range(100):
        suma += potencia_y / (2 * n + 1)
        potencia_y *= y2

        if valor_absoluto(potencia_y) < 1e-15:
            break

    return 2 * suma + k * 0.6931471805599453

# TRIGONOMETRIA

def _normalizar_angulo(x):
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    return x


def seno(x):
    x = _normalizar_angulo(x)

    suma = 0.0
    termino = x

    for n in range(1, 50):
        suma += termino
        termino *= -x * x / ((2 * n) * (2 * n + 1))

        if valor_absoluto(termino) < 1e-15:
            break

    return suma


def coseno(x):
    x = _normalizar_angulo(x)

    suma = 0.0
    termino = 1.0

    for n in range(1, 50):
        suma += termino
        termino *= -x * x / ((2 * n - 1) * (2 * n))

        if valor_absoluto(termino) < 1e-15:
            break

    return suma


def tangente(x):
    c = coseno(x)

    if valor_absoluto(c) < 1e-10:
        raise ValueError("tan(x) no definida en este punto")

    return seno(x) / c

# REGRESION LINEAL

def regresion_lineal(X, Y):
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

    denominador = n * sum_x2 - (sum_x * sum_x)

    if denominador == 0:
        raise ValueError("Division por cero en regresion")

    m = (n * sum_xy - sum_x * sum_y) / denominador
    b = (sum_y - m * sum_x) / n

    return [m, b]

# PREDICCION

def predecir(modelo, x):
    m, b = modelo
    return m * x + b

# ERROR 

def mse(X, Y, modelo):
    m, b = modelo
    n = len(X)

    error = 0.0

    for i in range(n):
        pred = m * X[i] + b
        error += (Y[i] - pred) ** 2

    return error / n
