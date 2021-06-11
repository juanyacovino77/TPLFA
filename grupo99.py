import ply.lex as lex

tokens = [
    'PALABRA',
    'NUMERO',
    'PAREN_IZQ',  # '('
    'PAREN_DER',  # ')'
    'COMA',  # ','
    'PUNTO',  # '.'
    'COMILLA',  # ' " '
    'IGUAL',  # '='
    'DESIGUAL',  # '<>'
    'MENOR_IZQ',  # '<'
    'MEN_IGUAL_IZQ',  # '<='
    'MAYOR_IZQ',  # '>'
    'MAY_IGUAL_IZQ'  # '>='
]
palabras_reservadas = {
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
    'BY' :'BY',
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
tokens = tokens + list(palabras_reservadas.values())
#reconocimiento por ER
t_ignore = ' \t'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_COMA = r','
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
    t.type = palabras_reservadas.get(t.value, 'PALABRA')
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


lexer = lex.lex() #instancio el lexer


tablas = {} #Guardo nombre y alias de las tablas
columnas = {} #Diccionario de listas, donde la key es la PALABRA antes del PUNTO
                 #y el valor es la lista de las columnas que comparten esa PALABRA

def p_consulta(p):
    '''
    consulta : SELECT distinct campos FROM tablas join where grupos order_by
    distinct : DISTINCT
    distinct :
    campos : columna
    campos : funcion
    campos : columna COMA campos
    campos : funcion COMA campos
    tablas : tabla
    tablas : tabla COMA tablas
    columnas : columna
    columnas : columna COMA columnas
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
    order_by :
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
def p_tabla(p):
    '''
    tabla : PALABRA
    tabla : PALABRA AS PALABRA
    tabla : PALABRA PALABRA
    '''
    if len(p) == 2:
        tablas.setdefault(p[1],p[1])
    elif len(p) == 4:
        tablas.setdefault(p[3],p[1])
    elif len(p) == 3:
        tablas.setdefault(p[2],p[1])
def p_columa(p):
    '''
    columna : PALABRA PUNTO PALABRA
    columna : PALABRA PUNTO PALABRA AS PALABRA
    '''
    lista_columna =columnas.get(p[1])

    if lista_columna is not None: #Si ya está registrada la tabla
        if p[3] not in lista_columna:
            lista_columna.append(p[3]) #Agrego la columna a la lista de esa tabla
    else: #Si no está registrada la tabla
        columnas.setdefault(p[1], [p[3]])  #La registro junto a la columna que ya trae
def p_error(p):
    print("Error sintáctico detectado")

##################################################### fin analizador


import ply.yacc as yacc

def parse_select_statement(s):
    analizador = yacc.yacc()
    analizador.parse(s)

    tablas_alias = tablas.keys() #Lista de los alias de las tablas
    tablas_columnas = columnas.keys() #Lista de llaves, que son las tablas que preceden a las columnas

    diferencia = set(tablas_alias) ^ set(tablas_columnas)

    if len(diferencia) > 0:
        raise NameError('Error, se estan usando tablas nunca definidas')
    else:
        #generamos un nuevo diccionario ya que modificar las claves del diccionarios parece imposible
        diccionario= {}
        for key in columnas:
            lista = columnas[key]
            nueva_key = tablas.get(key)
            diccionario.setdefault(nueva_key,lista)


        #ordenar alfabeticamente
        for lista in diccionario.values():
            lista.sort()

        return diccionario

