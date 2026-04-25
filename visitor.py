import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

from generated.DeepLangVisitor import DeepLangVisitor
from entorno import Entorno
import matematica as mat
import matrices as mx


class FuncionUsuario:
    def __init__(self, parametros, cuerpo, entorno_closure):
        self.parametros = parametros
        self.cuerpo = cuerpo
        self.entorno_closure = entorno_closure


class EjecutorDeepLang(DeepLangVisitor):

    def __init__(self):
        self.entorno = Entorno()
        self.modulos_importados = set()

        # =========================
        # MODULOS DEL DSL
        # =========================

        self.modulos = {
            "core": {
                'mostrar': lambda args: print(self._fmt(args[0])),
                'sen': lambda args: mat.seno(args[0]),
                'cos': lambda args: mat.coseno(args[0]),
                'tan': lambda args: mat.tangente(args[0]),
                'raiz': lambda args: mat.raiz(args[0]),
                'raizn': lambda args: mat.raiz(args[0], int(args[1])),
                'abs': lambda args: mat.valor_absoluto(args[0]),
                'exp': lambda args: mat.exponencial(args[0]),
                'ln': lambda args: mat.logaritmo_natural(args[0]),

                # 🔥 NUEVO
                'linreg': lambda args: mat.regresion_lineal(args[0], args[1]),
                'predict': lambda args: mat.predecir(args[0], args[1]),
            },

            "linalg": {
                'trans': lambda args: mx.transpuesta(args[0]),
                'inv': lambda args: mx.inversa(args[0]),
                'mostrar_mat': lambda args: mx.mostrar_mat(args[0]),
                'dim': lambda args: list(mx.dimensiones(args[0])),
            }
        }

    # =========================
    # IMPORTS
    # =========================

    def visitImportarStmt(self, ctx):
        nombre = ctx.ID(0).getText()
        alias = ctx.ID(1).getText() if len(ctx.ID()) > 1 else nombre

        if alias in self.modulos_importados:
            raise RuntimeError(f"Modulo '{alias}' ya fue importado")

        if nombre not in self.modulos:
            raise RuntimeError(f"Modulo '{nombre}' no existe")

        self.modulos_importados.add(alias)

        # guardar modulo como objeto
        self.entorno.definir(alias, self.modulos[nombre])

    def visitFromImportStmt(self, ctx):
        modulo = ctx.ID().getText()

        if modulo not in self.modulos:
            raise RuntimeError(f"Modulo '{modulo}' no existe")

        for fn_token in ctx.listaImport().ID():
            fn = fn_token.getText()

            if fn not in self.modulos[modulo]:
                raise RuntimeError(f"'{fn}' no existe en '{modulo}'")

            if fn in self.entorno._tabla:
                raise RuntimeError(f"Conflicto: '{fn}' ya existe")

            self.entorno.definir(fn, self.modulos[modulo][fn])

    # =========================
    # ACCESO MODULO (c.sen)
    # =========================

    def visitAccesoModuloExpr(self, ctx):
        modulo = ctx.ID(0).getText()
        funcion = ctx.ID(1).getText()

        mod = self.entorno.obtener(modulo)

        if not isinstance(mod, dict):
            raise RuntimeError(f"'{modulo}' no es un modulo")

        if funcion not in mod:
            raise RuntimeError(f"'{funcion}' no existe en '{modulo}'")

        return mod[funcion]

    # =========================
    # LLAMADAS
    # =========================

    def visitLlamadaFuncion(self, ctx):
        fn = self.visit(ctx.getChild(0))

        args = []
        if ctx.argumentos():
            args = [self.visit(e) for e in ctx.argumentos().expresion()]

        if callable(fn):
            return fn(args)

        if isinstance(fn, FuncionUsuario):
            if len(args) != len(fn.parametros):
                raise RuntimeError(
                    f"Funcion espera {len(fn.parametros)} argumentos, "
                    f"recibio {len(args)}"
                )

            nuevo_env = fn.entorno_closure.nuevo_ambito()
            for p, v in zip(fn.parametros, args):
                nuevo_env.definir(p, v)

            env_anterior = self.entorno
            self.entorno = nuevo_env
            resultado = self.visit(fn.cuerpo)
            self.entorno = env_anterior
            return resultado

        raise RuntimeError("No es una funcion")

    # =========================
    # PROGRAMA
    # =========================

    def visitPrograma(self, ctx):
        resultado = None
        for instr in ctx.instruccion():
            resultado = self.visit(instr)
        return resultado

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    # =========================
    # DECLARACIONES
    # =========================

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expresion())
        self.entorno.definir(nombre, valor)
        return valor

    # =========================
    # EXPRESIONES
    # =========================

    def visitExpSuma(self, ctx):
        return self.visit(ctx.expresionAdd()) + self.visit(ctx.expresionMult())

    def visitExpResta(self, ctx):
        return self.visit(ctx.expresionAdd()) - self.visit(ctx.expresionMult())

    def visitExpMult(self, ctx):
        return self.visit(ctx.expresionMult()) * self.visit(ctx.expresionPot())

    def visitExpDiv(self, ctx):
        divisor = self.visit(ctx.expresionPot())
        if divisor == 0:
            raise RuntimeError("Division por cero")
        return self.visit(ctx.expresionMult()) / divisor

    def visitExpMod(self, ctx):
        return self.visit(ctx.expresionMult()) % self.visit(ctx.expresionPot())

    def visitExpPot(self, ctx):
        return mat.potencia(
            self.visit(ctx.expresionUnaria()),
            self.visit(ctx.expresionPot())
        )

    def visitExpNeg(self, ctx):
        return -self.visit(ctx.expresionPrimaria())

    def visitExpNo(self, ctx):
        return not self.visit(ctx.expresionPrimaria())

    # =========================
    # LITERALES
    # =========================

    def visitLitNum(self, ctx):
        return float(ctx.NUM().getText())

    def visitVarId(self, ctx):
        return self.entorno.obtener(ctx.ID().getText())

    def visitLitMat(self, ctx):
        return self.visit(ctx.matriz())

    def visitMatriz(self, ctx):
        return [self.visit(f) for f in ctx.fila()]

    def visitFila(self, ctx):
        return [self.visit(e) for e in ctx.expresion()]

    def visitExpAgrup(self, ctx):
        return self.visit(ctx.expresion())

    # =========================
    # FORMATO
    # =========================

    def _fmt(self, valor):
        if isinstance(valor, list):
            return str(valor)
        if isinstance(valor, float) and valor == int(valor):
            return str(int(valor))
        return str(valor)
