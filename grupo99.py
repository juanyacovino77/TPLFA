import ply.lex as lex

tokens = [
    'PALABRA',
    'NUMERO',
    'PAREN_IZQ',  # '('
    'PAREN_DER',  # ')'
    'COMA',  # ','
    'PUNTOCOMA',  # ';'
    'PUNTO',  # '.'
    'COMILLA',  # ' " '
    'IGUAL',  # '='
    'DESIGUAL',  # '<>'
    'MENOR_IZQ',  # '<'
    'MEN_IGUAL_IZQ',  # '<='
    'MAYOR_IZQ',  # '>'
    'MAY_IGUAL_IZQ'  # '>='
]

reserved = {
    'SELECT': 'SELECT',
    'FROM': 'FROM',
    'WHERE': 'WHERE',
    'ON': 'ON',
    'IN': 'IN',
    'AS': 'AS',
    'INNER': 'INNER',
    'JOIN': 'JOIN',
    'LEFT': 'LEFT',
    'GROUP': 'GROUP',
    'ORDER': 'ORDER',
    'BY' : 'BY',
    'HAVING': 'HAVING',
    'MIN': 'MIN',
    'MAX': 'MAX',
    'COUNT': 'COUNT',
    'DISTINCT': 'DISTINCT',
    'AND': 'AND',
    'OR': 'OR',
    'ASC': 'ASC',
    'DESC': 'DESC'
}

tokens = tokens + list(reserved.values())


#expresiones regulares para token
t_ignore = ' \t'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_COMA = r','
t_PUNTOCOMA = r';'
t_PUNTO = r'\.'
t_COMILLA = r'"'
t_IGUAL = r'='
t_DESIGUAL = r'<>'
t_MENOR_IZQ = r'<'
t_MEN_IGUAL_IZQ = r'<='
t_MAYOR_IZQ = r'>'
t_MAY_IGUAL_IZQ = r'>='


def t_PALABRA(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'PALABRA')
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#instanciamos el lexer
lexer = lex.lex()


#data = 'select P.apellido as perro, P.nombre from persona as P, WHERE count max min and or, GROUP BY ORDER BY HAVING'
#lexer.input(data)

#while True:
#    token = lexer.token()
#    if not token:
#        break
#    print(token)



def p_consulta(p):
    '''
    consulta : SELECT campos FROM tablas join where grupos order_by

    campos : columna
    campos : funcion
    campos : columna COMA campos
    campos : funcion COMA campos

    tablas : tabla
    tablas : tabla COMA tablas
    tabla : PALABRA
    tabla : PALABRA AS PALABRA
    tabla : PALABRA PALABRA

    columnas : columna
    columnas : columna COMA columnas
    columna : PALABRA PUNTO PALABRA
    columna : PALABRA PUNTO PALABRA AS PALABRA

    funcion : MIN PAREN_IZQ columna PAREN_DER
    funcion : MAX PAREN_IZQ columna PAREN_DER
    funcion : COUNT PAREN_IZQ columna PAREN_DER
    funcion : COUNT PAREN_IZQ DISTINCT columna PAREN_DER

    join : INNER JOIN tabla ON condicion join
    join : LEFT JOIN tabla ON condicion join
    join :

    where : WHERE condiciones
    where :

    grupos : group_by
    grupos : group_by having
    grupos :

    group_by : GROUP BY columnas

    having : HAVING condiciones_having
    condiciones_having : funcion operador valor
    condiciones_having : funcion operador valor COMA condiciones_having

    order_by : ORDER BY condiciones_orderby
    condiciones_orderby : columna orden
    condiciones_orderby : columna orden COMA condiciones_orderby

    condiciones : condicion
    condiciones : condicion booleano condiciones
    condicion : columna operador valor
    condicion : columna operador columna
    condicion : columna IN PAREN_IZQ consulta PAREN_DER

    valor : NUMERO
    valor : COMILLA PALABRA COMILLA

    operador : IGUAL
    operador : DESIGUAL
    operador : MENOR_IZQ
    operador : MEN_IGUAL_IZQ
    operador : MAYOR_IZQ
    operador : MAY_IGUAL_IZQ

    booleano : AND
    booleano : OR

    orden : ASC
    orden : DESC
    orden :


    '''



def p_error(p):
    print("Error sintáctico detectado")


import ply.yacc as yacc

parser = yacc.yacc()


while True:
    try:
        s = input("analizador >")
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)


