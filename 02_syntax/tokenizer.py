import ply.lex as lex

# List of token names. This is always required
tokens = [
    # 'COMMENT',

    'LARROW',
    'RARROW',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',

    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',

    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'varIDENT',
    'constIDENT',
    'tupleIDENT',
    'funcIDENT'
]

# list of reserved words
reserved = {
    'define': 'DEFINE',
    'begin': 'BEGIN',
    'end': 'END',
    'each': 'EACH',
    'select': 'SELECT'
}
tokens += reserved.values()

# Regular expression rules for simple tokens
t_LARROW = r'\<-'
t_RARROW = r'\->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r'\,'
t_DOT = r'\.'
t_PIPE = r'\|'
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEDOT = r'\.\.'
t_COLON = r'\:'

t_EQ = r'\='
t_NOTEQ = r'\!='
t_LT = r'\<'
t_LTEQ = r'\<='
t_GT = r'\>'
t_GTEQ = r'\>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT= r'\*'
t_DIV = r'/'
t_MOD = r'\%'

# a constant identifier contain one or more characters in 'A-Z'
t_constIDENT = r'[A-Z]+'
# a tuple variable starts with '<' and must be followed
# at least one lowercase char ('a-z'). The last char must be '>'.
t_tupleIDENT = r'[<][a-z]+[>]'
# a function name starts with an uppercase letter (A-Z) and
# must be followed by at least one character in
# set( 'a-z', '0-9', '_' ). NOTE that this does not allow
# one letter function names
t_funcIDENT = r'[A-Z][a-z0-9_]+'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A regular expression rule with some action code
def t_NUMBER_LITERAL(t):
    r'\d+'  # find digits
    t.value = int(t.value)
    return t


# STRING_LITERAL: a string consists of a quote mark "
# followed by zero or more of either an escaped anything \\.
# or (|) a non-quote character [^"\\]
# and finally a terminating quote ". Put them all together we get:
def t_STRING_LITERAL(t):
    r'\"(\\.|[^"\\])*\"'
    t.value = t.value.strip('\"')
    return t


# varIDENT: a variable name starts with a lowercase letter (a-z) and
# must be followed by at least one character in
# set( 'a-z', 'A-Z', '0-9', '_' ).
# NOTE that this does not allow one letter variable names.
def t_varIDENT(t):
    r'[a-z]+[a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


# def t_ID(t):
#     r'[a-zA-Z_][a-zA-Z_0-9]*'
#     # r'define|begin|end|each|select'
#     t.type = reserved[t.value]
#     return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \r'
t_ignore_COMMENT = r'\{.*}'


# def t_COMMENT(t):
#     r'\{.*}'
#     pass


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
