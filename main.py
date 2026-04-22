import sys
from antlr4 import CommonTokenStream, FileStream

from generated.DeepLangLexer import DeepLangLexer
from generated.DeepLangParser import DeepLangParser

from errores import ErrorSintaxis
from visitor import EjecutorDeepLang


def construir_parser(ruta_archivo):
    flujo = FileStream(ruta_archivo, encoding='utf-8')

    lexer = DeepLangLexer(flujo)
    tokens = CommonTokenStream(lexer)
    parser = DeepLangParser(tokens)

    # Manejo de errores
    listener = ErrorSintaxis()
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    lexer.addErrorListener(listener)
    parser.addErrorListener(listener)

    return parser


def ejecutar_archivo(ruta_archivo):
    parser = construir_parser(ruta_archivo)
    arbol = parser.programa()

    visitor = EjecutorDeepLang()
    visitor.visit(arbol)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo.dl>")
        sys.exit(1)

    ruta = sys.argv[1]

    try:
        ejecutar_archivo(ruta)
    except (RuntimeError, SyntaxError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
