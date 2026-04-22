grammar DeepLang;

programa
    : instruccion* EOF
    ;

instruccion
    : declaracion
    | expresionStmt
    | defFuncion
    | importarStmt
    | fromImportStmt
    ;

importarStmt
    : IMPORTAR ID (COMO ID)?
    ;

fromImportStmt
    : FROM ID IMPORT listaImport
    ;

listaImport
    : ID (COMA ID)*
    ;

declaracion
    : LET ID DOBLESDOS tipo ASIG expresion
    ;

tipo
    : TNUM
    | TTEXTO
    | TBOOL
    | TMAT
    ;

defFuncion
    : DEFN ID DOBLESDOS tipoFuncion
      PIPE parametros FLECHA expresion
      FIN
    ;

tipoFuncion
    : tipo (RARROW tipo)*
    ;

parametros
    : ID (COMA ID)*
    ;

expresionStmt
    : expresion
    ;

expresion
    : expresion OROP expresionAnd          # expOr
    | expresionAnd                         # expAndPass
    ;

expresionAnd
    : expresionAnd ANDOP expresionComp     # expAnd
    | expresionComp                        # expCompPass
    ;

expresionComp
    : expresionComp opComp expresionAdd    # expComp
    | expresionAdd                         # expAddPass
    ;

expresionAdd
    : expresionAdd PLUS  expresionMult     # expSuma
    | expresionAdd MINUS expresionMult     # expResta
    | expresionAdd MATADD expresionMult    # expMatSuma
    | expresionAdd MATSUB expresionMult    # expMatResta
    | expresionMult                        # expMultPass
    ;

expresionMult
    : expresionMult TIMES  expresionPot    # expMult
    | expresionMult DIV    expresionPot    # expDiv
    | expresionMult MOD    expresionPot    # expMod
    | expresionMult MATMUL expresionPot    # expMatMult
    | expresionPot                         # expPotPass
    ;

expresionPot
    : expresionUnaria POW expresionPot     # expPot
    | expresionUnaria                      # expUnPass
    ;

expresionUnaria
    : MINUS expresionPrimaria              # expNeg
    | NO    expresionPrimaria              # expNo
    | expresionPrimaria                    # expPrimPass
    ;

expresionPrimaria
    : NUM                                  # litNum
    | TEXTO                                # litTexto
    | VERDAD                               # litVerdad
    | FALSO                                # litFalso
    | ID                                   # varId
    | accesoModulo                         # accesoModuloExpr
    | matriz                               # litMat
    | llamadaFuncion                       # expLlamada
    | LPAREN expresion RPAREN              # expAgrup
    ;

accesoModulo
    : ID DOT ID
    ;

matriz
    : LBRAC fila (COMA fila)* RBRAC
    ;

fila
    : LBRAC expresion (COMA expresion)* RBRAC
    ;

llamadaFuncion
    : (ID | accesoModulo) LPAREN argumentos? RPAREN
    ;

argumentos
    : expresion (COMA expresion)*
    ;

opComp
    : EQEQ | NEQ | LT | GT | LEQ | GEQ
    ;

IMPORTAR : 'importar';
COMO     : 'como';
FROM     : 'from';
IMPORT   : 'import';
DOT      : '.';

LET       : 'sea';
DEFN      : 'defn';
FIN       : 'fin';
PIPE      : '|';
FLECHA    : '=>';
RARROW    : '->';
DOBLESDOS : '::';
ASIG      : '=';

TNUM      : 'Num';
TTEXTO    : 'Texto';
TBOOL     : 'Bool';
TMAT      : 'Mat';

VERDAD    : 'verdad';
FALSO     : 'falso';

OROP      : 'o';
ANDOP     : 'y';
NO        : 'no';

PLUS      : '+';
MINUS     : '-';
TIMES     : '*';
DIV       : '/';
MOD       : '%';
POW       : '^';

MATADD    : '|+|';
MATSUB    : '|-|';
MATMUL    : '|*|';

EQEQ      : '==';
NEQ       : '!=';
LT        : '<';
GT        : '>';
LEQ       : '<=';
GEQ       : '>=';

LPAREN    : '(';
RPAREN    : ')';
LBRAC     : '[';
RBRAC     : ']';

NUM       : [0-9]+ ('.' [0-9]+)?;
TEXTO     : '"' (~["\r\n])* '"';
ID        : [a-zA-Z_][a-zA-Z0-9_]*;

COMENTARIO : '(*' .*? '*)' -> skip;
WS         : [ \t\r\n]+ -> skip;
