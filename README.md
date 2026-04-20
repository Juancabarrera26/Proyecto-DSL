# DeepLang

DSL funcional orientado a operaciones de Deep Learning, implementado con ANTLRv4 y Python.

## Requisitos

- Python 3.8 o superior
- Java 11 o superior (para correr el generador de ANTLR)
- Ubuntu / Linux (recomendado)

## Instalacion

```bash
# 1. Instalar dependencias del sistema
sudo apt update && sudo apt install -y default-jre python3 python3-pip

# 2. Instalar el runtime de ANTLR para Python
pip3 install antlr4-python3-runtime==4.13.1

# 3. Descargar el generador ANTLR4
wget https://www.antlr.org/download/antlr-4.13.1-complete.jar -O antlr4.jar
```

## Generar el parser

Desde la raiz del proyecto ejecutar:

```bash
java -jar antlr4.jar -Dlanguage=Python3 -visitor -o generated DeepLang.g4
```

Esto sobreescribe los archivos en `generated/` con el lexer, parser y visitor base generados por ANTLR.

## Ejecutar programas

```bash
python3 main.py ejemplos/aritmetica.dl
python3 main.py ejemplos/matrices.dl
python3 main.py ejemplos/funciones.dl
```

## Estructura del proyecto

```
deeplang/
├── DeepLang.g4       <- Gramatica formal del lenguaje
├── main.py           <- Punto de entrada
├── visitor.py        <- Evaluador (patron Visitor)
├── entorno.py        <- Tabla de simbolos con ambitos anidados
├── errores.py        <- Listener de errores de sintaxis
├── matematica.py     <- Operaciones matematicas sin librerias externas
├── matrices.py       <- Operaciones matriciales sin librerias externas
├── ejemplos/
│   ├── aritmetica.dl
│   ├── matrices.dl
│   └── funciones.dl
└── generated/        <- Generado por ANTLR (no editar)
    ├── DeepLangLexer.py
    ├── DeepLangParser.py
    └── DeepLangVisitor.py
```

## Sintaxis basica

```
(* comentario *)

sea x :: Num = 10.0
sea M :: Mat = [[1.0, 2.0], [3.0, 4.0]]

defn cuadrado :: Num -> Num
  | n => n ^ 2.0
fin

mostrar(cuadrado(5.0))
mostrar_mat(trans(M))
mostrar_mat(inv(M))
```

## Operadores de matrices

| Operador | Operacion     |
|----------|---------------|
| `\|+\|`  | Suma          |
| `\|-\|`  | Resta         |
| `\|*\|`  | Multiplicacion|
| `trans`  | Transpuesta   |
| `inv`    | Inversa       |

## Funciones integradas

| Funcion       | Descripcion                  |
|---------------|------------------------------|
| `sen(x)`      | Seno                         |
| `cos(x)`      | Coseno                       |
| `tan(x)`      | Tangente                     |
| `raiz(x)`     | Raiz cuadrada                |
| `raizn(x, n)` | Raiz n-esima                 |
| `abs(x)`      | Valor absoluto               |
| `exp(x)`      | Exponencial e^x              |
| `ln(x)`       | Logaritmo natural            |
| `mostrar(x)`  | Imprime un valor             |
| `mostrar_mat` | Imprime una matriz           |
| `trans(M)`    | Transpuesta de M             |
| `inv(M)`      | Inversa de M                 |
| `dim(M)`      | Dimensiones de M             |
