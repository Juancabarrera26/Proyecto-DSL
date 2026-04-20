from antlr4.error.ErrorListener import ErrorListener


class ErrorSintaxis(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"[Linea {line}:{column}] {msg}")


class ErrorEjecucion(Exception):
    pass
