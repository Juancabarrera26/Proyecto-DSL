import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

from generated.DeepLangVisitor import DeepLangVisitor
from generated.DeepLangParser  import DeepLangParser
from entorno    import Entorno
import matematica as mat
import matrices   as mx


class FuncionUsuario:
    def __init__(self, parametros, cuerpo, entorno_closure):
        self.parametros       = parametros
        self.cuerpo           = cuerpo
        self.entorno_closure  = entorno_closure


class EjecutorDeepLang(DeepLangVisitor):

    def __init__(self):
        self.entorno = Entorno()
        self._registrar_builtins()

    def _registrar_builtins(self):
        builtins = {
            'mostrar'    : lambda args: print(self._fmt(args[0])),
            'sen'        : lambda args: mat.seno(args[0]),
            'cos'        : lambda args: mat.coseno(args[0]),
            'tan'        : lambda args: mat.tangente(args[0]),
            'raiz'       : lambda args: mat.raiz(args[0]),
            'raizn'      : lambda args: mat.raiz(args[0], int(args[1])),
            'abs'        : lambda args: mat.valor_absoluto(args[0]),
            'exp'        : lambda args: mat.exponencial(args[0]),
            'ln'         : lambda args: mat.logaritmo_natural(args[0]),
            'trans'      : lambda args: mx.transpuesta(args[0]),
            'inv'        : lambda args: mx.inversa(args[0]),
            'mostrar_mat': lambda args: mx.mostrar_mat(args[0]),
            'dim'        : lambda args: list(mx.dimensiones(args[0])),
        }
        for nombre, fn in builtins.items():
            self.entorno.definir(nombre, fn)

    def _fmt(self, valor):
        if isinstance(valor, list):
            return str(valor)
        if isinstance(valor, float) and valor == int(valor):
            return str(int(valor))
        return str(valor)

    # programa

    def visitPrograma(self, ctx):
        resultado = None
        for instr in ctx.instruccion():
            resultado = self.visit(instr)
        return resultado

    def visitInstruccion(self, ctx):
        return self.visitChildren(ctx)

    # declaraciones

    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()
        valor  = self.visit(ctx.expresion())
        self.entorno.definir(nombre, valor)
        return valor

    # funciones

    def visitDefFuncion(self, ctx):
        nombre = ctx.ID().getText()
        params = [p.getText() for p in ctx.parametros().ID()]
        cuerpo = ctx.expresion()
        fn     = FuncionUsuario(params, cuerpo, self.entorno)
        self.entorno.definir(nombre, fn)
        return fn

    def visitExpLlamada(self, ctx):
        return self.visitLlamadaFuncion(ctx.llamadaFuncion())

    def visitLlamadaFuncion(self, ctx):
        nombre = ctx.ID().getText()
        fn     = self.entorno.obtener(nombre)
        args   = []
        if ctx.argumentos():
            args = [self.visit(e) for e in ctx.argumentos().expresion()]

        if callable(fn):
            return fn(args)

        if isinstance(fn, FuncionUsuario):
            if len(args) != len(fn.parametros):
                raise RuntimeError(
                    f"'{nombre}' espera {len(fn.parametros)} argumentos, "
                    f"recibio {len(args)}"
                )
            nuevo_env = fn.entorno_closure.nuevo_ambito()
            for p, v in zip(fn.parametros, args):
                nuevo_env.definir(p, v)
            env_anterior   = self.entorno
            self.entorno   = nuevo_env
            resultado      = self.visit(fn.cuerpo)
            self.entorno   = env_anterior
            return resultado

        raise RuntimeError(f"'{nombre}' no es una funcion")

    # aritmetica

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
        base = self.visit(ctx.expresionUnaria())
        exp  = self.visit(ctx.expresionPot())
        return mat.potencia(base, exp)

    def visitExpNeg(self, ctx):
        return -self.visit(ctx.expresionPrimaria())

    def visitExpNo(self, ctx):
        return not self.visit(ctx.expresionPrimaria())

    # matrices

    def visitExpMatSuma(self, ctx):
        return mx.suma_mat(
            self.visit(ctx.expresionAdd()),
            self.visit(ctx.expresionMult())
        )

    def visitExpMatResta(self, ctx):
        return mx.resta_mat(
            self.visit(ctx.expresionAdd()),
            self.visit(ctx.expresionMult())
        )

    def visitExpMatMult(self, ctx):
        return mx.mult_mat(
            self.visit(ctx.expresionMult()),
            self.visit(ctx.expresionPot())
        )

    # comparaciones y logica

    def visitExpComp(self, ctx):
        izq = self.visit(ctx.expresionComp())
        der = self.visit(ctx.expresionAdd())
        op  = ctx.opComp().getText()
        tabla = {
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<' : lambda a, b: a <  b,
            '>' : lambda a, b: a >  b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
        }
        return tabla[op](izq, der)

    def visitExpOr(self, ctx):
        return self.visit(ctx.expresion()) or self.visit(ctx.expresionAnd())

    def visitExpAnd(self, ctx):
        return self.visit(ctx.expresionAnd()) and self.visit(ctx.expresionComp())

    # literales

    def visitLitNum(self, ctx):
        return float(ctx.NUM().getText())

    def visitLitTexto(self, ctx):
        return ctx.TEXTO().getText()[1:-1]

    def visitLitVerdad(self, ctx):
        return True

    def visitLitFalso(self, ctx):
        return False

    def visitVarId(self, ctx):
        return self.entorno.obtener(ctx.ID().getText())

    def visitExpAgrup(self, ctx):
        return self.visit(ctx.expresion())

    def visitLitMat(self, ctx):
        return self.visit(ctx.matriz())

    def visitMatriz(self, ctx):
        return [self.visit(f) for f in ctx.fila()]

    def visitFila(self, ctx):
        return [self.visit(e) for e in ctx.expresion()]

    # pases de precedencia

    def visitExpAndPass(self, ctx):  return self.visitChildren(ctx)
    def visitExpCompPass(self, ctx): return self.visitChildren(ctx)
    def visitExpAddPass(self, ctx):  return self.visitChildren(ctx)
    def visitExpMultPass(self, ctx): return self.visitChildren(ctx)
    def visitExpPotPass(self, ctx):  return self.visitChildren(ctx)
    def visitExpUnPass(self, ctx):   return self.visitChildren(ctx)
    def visitExpPrimPass(self, ctx): return self.visitChildren(ctx)
    def visitExpresionStmt(self, ctx): return self.visitChildren(ctx)
