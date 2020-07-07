from ply import yacc
import tokenizer  # previous phase example snippet code

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = tokenizer.tokens


# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : zero_or_more_func_or_var_def return_value DOT'''
    # print('program')


def p_zero_or_more_func_or_var_def(p):
    '''zero_or_more_func_or_var_def : function_or_variable_definition zero_or_more_func_or_var_def'''


def p_zero_or_more_func_or_var_def2(p):
    '''zero_or_more_func_or_var_def : '''


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions'''


def p_function_or_variable_definition2(p):
    '''function_or_variable_definition : function_definition'''


def p_zero_or_more_variable_definitions(p):
    '''zero_or_more_variable_definitions : variable_definitions zero_or_more_variable_definitions'''


def p_zero_or_more_variable_definitions2(p):
    '''zero_or_more_variable_definitions : '''


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN zero_or_more_variable_definitions return_value DOT END DOT'''
    print('func_definition(', p[2], ')')


def p_function_definition2(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE BEGIN zero_or_more_variable_definitions return_value DOT END DOT'''
    print('func_definition(', p[2], ')')


def p_zero_or_more_comma_var_ident(p):
    '''zero_or_more_comma_var_ident : COMMA varIDENT zero_or_more_comma_var_ident'''


def p_zero_or_more_comma_var_ident2(p):
    '''zero_or_more_comma_var_ident : '''


def p_formals(p):
    '''formals : varIDENT zero_or_more_comma_var_ident'''


def p_return_value(p):
    '''return_value : EQ simple_expression'''


def p_return_value2(p):
    '''return_value : NOTEQ pipe_expression'''


def p_variable_definitions(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT'''
    print('variable_definition(', p[1], ')')


def p_variable_definitions2(p):
    '''variable_definitions : constIDENT LARROW constant_expression DOT'''
    print('constant_definition(', p[1], ')')


def p_variable_definitions3(p):
    '''variable_definitions : tupleIDENT LARROW tuple_expression DOT'''
    print('tuplevariable_definition(', p[1], ')')


def p_variable_definitions4(p):
    '''variable_definitions : pipe_expression RARROW tupleIDENT DOT '''
    print('tuplevariable_definition(', p[3], ')')


def p_constant_expression(p):
    '''constant_expression : constIDENT'''


def p_constant_expression2(p):
    '''constant_expression : NUMBER_LITERAL'''


def p_zero_or_more_pipe_pipe_op(p):
    '''zero_or_more_pipe_pipe_op : PIPE pipe_operation zero_or_more_pipe_pipe_op'''


def p_zero_or_more_pipe_pipe_op2(p):
    '''zero_or_more_pipe_pipe_op : '''


def p_pipe_expression(p):
    '''pipe_expression : tuple_expression zero_or_more_pipe_pipe_op'''
    print('pipe_expression')


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT'''


def p_pipe_operation2(p):
    '''pipe_operation : MULT'''


def p_pipe_operation3(p):
    '''pipe_operation : PLUS'''


def p_pipe_operation4(p):
    '''pipe_operation : each_statement'''


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''


def p_zero_or_more_tup_op_tup_atom(p):
    '''zero_or_more_tup_op_tup_atom : tuple_operation tuple_atom zero_or_more_tup_op_tup_atom'''


def p_zero_or_more_tup_op_tup_atom2(p):
    '''zero_or_more_tup_op_tup_atom : '''


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom zero_or_more_tup_op_tup_atom'''
    # print('tuplevariable_definition(', p[0], ')')


def p_tuple_operation(p):
    '''tuple_operation ::= DOUBLEPLUS'''


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT'''
    print('tuplevariable_definition(', p[1], ')')


def p_tuple_atom2(p):
    '''tuple_atom : function_call'''


def p_tuple_atom3(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE'''


def p_tuple_atom4(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE'''


def p_tuple_atom5(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    print('function_call( ', p[1], ')')


def p_function_call2(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    print('function_call( ', p[1], ')')


def p_zero_or_more_comma_simple_expression(p):
    '''zero_or_more_comma_simple_expression : COMMA simple_expression zero_or_more_comma_simple_expression'''


def p_zero_or_more_comma_simple_expression2(p):
    '''zero_or_more_comma_simple_expression : '''


def p_arguments(p):
    '''arguments : simple_expression zero_or_more_comma_simple_expression'''


def p_printed_atoms(p):
    '''printed_atoms : NUMBER_LITERAL
                     | STRING_LITERAL
                     | varIDENT
                     | constIDENT'''
    print('atom(', p[1], ')')


def p_atom(p):
    '''atom : function_call'''


def p_atom2(p):
    '''atom : printed_atoms'''


def p_atom3(p):
    '''atom : LPAREN simple_expression RPAREN'''
    print('atom')


def p_atom4(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    print('atom')


def p_factor(p):
    '''factor : atom'''
    print('factor')


def p_factor2(p):
    '''factor : MINUS atom'''
    print('factor')


def p_zero_or_more_mult_factor(p):
    '''zero_or_more_mult_factor : MULT factor zero_or_more_mult_factor'''


def p_zero_or_more_mult_factor2(p):
    '''zero_or_more_mult_factor : '''


def p_zero_or_more_div_factor(p):
    '''zero_or_more_div_factor : DIV factor zero_or_more_div_factor'''


def p_zero_or_more_div_factor2(p):
    '''zero_or_more_div_factor : '''


def p_term(p):
    '''term : factor'''
    print('term')


def p_term2(p):
    '''term : factor zero_or_more_div_factor'''
    print('term')


def p_term3(p):
    '''term : factor zero_or_more_mult_factor'''
    print('term')


def p_zero_or_more_minus_term(p):
    '''zero_or_more_minus_term : MINUS term zero_or_more_minus_term'''


def p_zero_or_more_minus_term2(p):
    '''zero_or_more_minus_term : '''


def p_zero_or_more_plus_term(p):
    '''zero_or_more_plus_term : PLUS term zero_or_more_plus_term'''


def p_zero_or_more_plus_term2(p):
    '''zero_or_more_plus_term : '''


# def p_simple_expression(p):
#     '''simple_expression : term zero_or_more_plus_term
#                          | term zero_or_more_minus_term'''
#     print('simple_expression')


def p_simple_expression(p):
    '''simple_expression : term zero_or_more_plus_term'''
    # p[0] = ASTnode('simple_expression')
    print('simple_expression')


def p_simple_expression2(p):
    '''simple_expression : term zero_or_more_minus_term'''
    # p[0] = ASTnode('simple_expression')
    print('simple_expression')


# precedence = (
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'TIMES', 'DIVIDE'),
# )


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print('syntax error @', p)
    raise SystemExit


parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('Khoa Nguyen - 272580')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        if result is None:
            print('syntax OK')
