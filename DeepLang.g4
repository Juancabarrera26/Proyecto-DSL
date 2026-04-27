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
    : expresion OROP expresionAnd
    | expresionAnd
    ;

expresionAnd
    : expresionAnd ANDOP expresionComp
    | expresionComp
    ;

expresionComp
    : expresionComp opComp expresionAdd
    | expresionAdd
    ;

expresionAdd
    : expresionAdd PLUS expresionMult
    | expresionAdd MINUS expresionMult
    | expresionAdd MATADD expresionMult
    | expresionAdd MATSUB expresionMult
    | expresionMult
    ;

expresionMult
    : expresionMult TIMES expresionPot
    | expresionMult DIV expresionPot
    | expresionMult MATMUL expresionPot
    | expresionPot
    ;

expresionPot
    : expresionUnaria POW expresionPot
    | expresionUnaria
    ;

expresionUnaria
    : MINUS expresionPrimaria
    | NO expresionPrimaria
    | expresionPrimaria
    ;

expresionPrimaria
    : NUM
    | TEXTO
    | VERDAD
    | FALSO
    | ID
    | accesoModulo
    | matriz
    | llamadaFuncion
    | LPAREN expresion RPAREN
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

WS : [ \t\r\n]+ -> skip;
