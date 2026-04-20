def _validar(A):
    filas = len(A)
    if filas == 0:
        raise ValueError("La matriz esta vacia")
    cols = len(A[0])
    for fila in A:
        if len(fila) != cols:
            raise ValueError("Las filas tienen distinto numero de columnas")
    return filas, cols


def dimensiones(A):
    return _validar(A)


def ceros(filas, cols):
    return [[0.0] * cols for _ in range(filas)]


def identidad(n):
    M = ceros(n, n)
    for i in range(n):
        M[i][i] = 1.0
    return M


def suma_mat(A, B):
    f, c = _validar(A)
    fb, cb = _validar(B)
    if f != fb or c != cb:
        raise ValueError(f"Dimensiones incompatibles: {f}x{c} vs {fb}x{cb}")
    return [[A[i][j] + B[i][j] for j in range(c)] for i in range(f)]


def resta_mat(A, B):
    f, c = _validar(A)
    fb, cb = _validar(B)
    if f != fb or c != cb:
        raise ValueError(f"Dimensiones incompatibles: {f}x{c} vs {fb}x{cb}")
    return [[A[i][j] - B[i][j] for j in range(c)] for i in range(f)]


def mult_mat(A, B):
    fa, ca = _validar(A)
    fb, cb = _validar(B)
    if ca != fb:
        raise ValueError(f"No se pueden multiplicar matrices {fa}x{ca} y {fb}x{cb}")
    R = ceros(fa, cb)
    for i in range(fa):
        for j in range(cb):
            for k in range(ca):
                R[i][j] += A[i][k] * B[k][j]
    return R


def transpuesta(A):
    f, c = _validar(A)
    return [[A[i][j] for i in range(f)] for j in range(c)]


def inversa(A):
    n, c = _validar(A)
    if n != c:
        raise ValueError("Solo las matrices cuadradas tienen inversa")

    # Gauss-Jordan sobre la matriz aumentada [A | I]
    aug = [A[i][:] + identidad(n)[i] for i in range(n)]

    for col in range(n):
        pivote_fila = None
        for fila in range(col, n):
            if abs(aug[fila][col]) > 1e-10:
                pivote_fila = fila
                break
        if pivote_fila is None:
            raise ValueError("La matriz es singular y no tiene inversa")

        aug[col], aug[pivote_fila] = aug[pivote_fila], aug[col]

        factor = aug[col][col]
        aug[col] = [v / factor for v in aug[col]]

        for fila in range(n):
            if fila != col:
                f = aug[fila][col]
                aug[fila] = [aug[fila][j] - f * aug[col][j] for j in range(2 * n)]

    return [fila[n:] for fila in aug]


def mostrar_mat(A, nombre=""):
    f, c = _validar(A)
    if nombre:
        print(f"Matriz {nombre} [{f}x{c}]:")
    for fila in A:
        print("  [" + "  ".join(f"{v:8.4f}" for v in fila) + "]")
