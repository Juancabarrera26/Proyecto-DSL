import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

from antlr4 import CommonTokenStream, FileStream

from generated.DeepLangLexer  import DeepLangLexer
from generated.DeepLangParser import DeepLangParser
from errores  import ErrorSintaxis
from visitor  import EjecutorDeepLang


def ejecutar(ruta):
    flujo  = FileStream(ruta, encoding='utf-8')
    lexer  = DeepLangLexer(flujo)
    tokens = CommonTokenStream(lexer)
    parser = DeepLangParser(tokens)

    listener = ErrorSintaxis()
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    lexer.addErrorListener(listener)
    parser.addErrorListener(listener)

    arbol   = parser.programa()
    visitor = EjecutorDeepLang()

    try:
        visitor.visit(arbol)
    except (RuntimeError, SyntaxError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo.dl>")
        sys.exit(1)
    ejecutar(sys.argv[1])
