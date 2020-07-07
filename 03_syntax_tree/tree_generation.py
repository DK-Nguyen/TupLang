from ply import yacc
import tokenizer
import tree_print  # syntax tree printer

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = tokenizer.tokens


class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr


# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : zero_or_more_func_or_var_def return_value DOT'''
    p[0] = ASTnode('program')
    p[0].child_func_or_var_defs = p[1]
    p[0].child_return_value = p[2]


def p_zero_or_more_func_or_var_def1(p):
    '''zero_or_more_func_or_var_def : function_or_variable_definition'''
    p[0] = ASTnode('')
    p[0].children_definitions = [p[1]]


def p_zero_or_more_func_or_var_def2(p):
    '''zero_or_more_func_or_var_def : function_or_variable_definition zero_or_more_func_or_var_def'''
    p[0] = p[2]
    p[0].children_definitions.insert(0, p[1])


def p_zero_or_more_func_or_var_def3(p):
    '''zero_or_more_func_or_var_def : '''


def p_function_or_variable_definition(p):
    '''function_or_variable_definition : variable_definitions'''
    p[0] = p[1]


def p_function_or_variable_definition2(p):
    '''function_or_variable_definition : function_definition'''
    p[0] = p[1]


def p_zero_or_more_variable_definitions(p):
    '''zero_or_more_variable_definitions : variable_definitions'''
    p[0] = ASTnode('')
    p[0].children_variable_definitions = [p[1]]
    # p[0] = [p[1]]


def p_zero_or_more_variable_definitions2(p):
    '''zero_or_more_variable_definitions : variable_definitions zero_or_more_variable_definitions'''
    p[0] = p[2]
    p[0].insert(0, p[1])


def p_zero_or_more_variable_definitions3(p):
    '''zero_or_more_variable_definitions : '''


def p_function_definition(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN zero_or_more_variable_definitions return_value DOT END DOT'''
    # print('func_definition(', p[2], ')')
    p[0] = ASTnode('function_definition')
    p[0].value = p[2]
    p[0].child_variable_definitions = p[7]
    p[0].child_simple_return_values = p[8]


def p_function_definition2(p):
    '''function_definition : DEFINE funcIDENT LSQUARE RSQUARE BEGIN zero_or_more_variable_definitions return_value DOT END DOT'''
    # print('func_definition(', p[2], ')')
    p[0] = ASTnode('function_definition')
    p[0].value = p[2]
    p[0].child_variable_definitions = p[6]
    p[0].child_return_values = p[7]


def p_zero_or_more_comma_var_ident(p):
    '''zero_or_more_comma_var_ident : COMMA varIDENT'''
    p[0] = ASTnode('')
    p[0].children_vars = [p[2]]


def p_zero_or_more_comma_var_ident2(p):
    '''zero_or_more_comma_var_ident : COMMA varIDENT zero_or_more_comma_var_ident'''
    p[0] = p[2]
    p[0].children_vars.insert(0, p[1])


def p_zero_or_more_comma_var_ident3(p):
    '''zero_or_more_comma_var_ident : '''


def p_formals(p):
    '''formals : varIDENT zero_or_more_comma_var_ident'''
    p[0] = ASTnode('formals')
    p[0].child_var = p[1]
    p[0].child_comma_var_ident = p[2]


def p_return_value(p):
    '''return_value : EQ simple_expression'''
    p[0] = ASTnode('simple_return_value')
    p[0].child_retval = p[2]


def p_return_value2(p):
    '''return_value : NOTEQ pipe_expression'''
    p[0] = ASTnode('not_equal_return_value')
    p[0].child_retval = p[2]


def p_variable_definitions(p):
    '''variable_definitions : varIDENT LARROW simple_expression DOT'''
    # print('variable_definition(', p[1], ')')
    p[0] = ASTnode('variable_definition')
    p[0].value = p[1]
    p[0].child_simple_expression = p[3]


def p_variable_definitions2(p):
    '''variable_definitions : constIDENT LARROW constant_expression DOT'''
    # print('constant_definition(', p[1], ')')
    p[0] = ASTnode('constant_definition')
    p[0].value = p[1]
    p[0].child_simple_expression = p[3]


def p_variable_definitions3(p):
    '''variable_definitions : tupleIDENT LARROW tuple_expression DOT'''
    # print('tuplevariable_definition(', p[1], ')')
    p[0] = ASTnode('tuplevariable_definition')
    p[0].value = p[1]
    p[0].child_simple_expression = p[3]


def p_variable_definitions4(p):
    '''variable_definitions : pipe_expression RARROW tupleIDENT DOT '''
    # print('tuplevariable_definition(', p[3], ')')
    # p[0] = ASTnode('tuplevariable_definition')
    p[0] = ASTnode('tuplevariable_definition')
    p[0].value = p[3]
    p[0].child_simple_expression = p[1]


def p_constant_expression(p):
    '''constant_expression : constIDENT'''
    p[0] = ASTnode('constIDENT')
    p[0].value = p[1]


def p_constant_expression2(p):
    '''constant_expression : NUMBER_LITERAL'''
    p[0] = ASTnode('NUMBER_LITERAL')
    p[0].value = p[1]


def p_zero_or_more_pipe_pipe_op(p):
    '''zero_or_more_pipe_pipe_op : PIPE pipe_operation'''
    p[0] = ASTnode('')
    p[0].children_pipe_operations = [p[2]]


def p_zero_or_more_pipe_pipe_op2(p):
    '''zero_or_more_pipe_pipe_op : PIPE pipe_operation zero_or_more_pipe_pipe_op'''
    p[0] = p[3]
    p[0].children_pipe_operations.insert(0, p[2])


def p_zero_or_more_pipe_pipe_op3(p):
    '''zero_or_more_pipe_pipe_op : '''


def p_pipe_expression(p):
    '''pipe_expression : tuple_expression zero_or_more_pipe_pipe_op'''
    # print('pipe_expression')
    p[0] = ASTnode('pipe_expression')
    p[0].child_tuple_expression = p[1]
    p[0].child_pipe_operations = p[2]


def p_pipe_operation(p):
    '''pipe_operation : funcIDENT'''
    p[0] = ASTnode('pipe_operation')
    p[0].value = p[1]


def p_pipe_operation2(p):
    '''pipe_operation : MULT'''
    p[0] = ASTnode('pipe_operation')
    p[0].value = p[1]


def p_pipe_operation3(p):
    '''pipe_operation : PLUS'''
    p[0] = ASTnode('pipe_operation')
    p[0].value = p[1]


def p_pipe_operation4(p):
    '''pipe_operation : each_statement'''
    p[0] = ASTnode('pipe_operation')
    p[0].child_each_statement = p[1]


def p_each_statement(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = ASTnode('each_statement')
    p[0].value = p[3]


def p_zero_or_more_tup_op_tup_atom(p):
    '''zero_or_more_tup_op_tup_atom : tuple_operation tuple_atom'''
    p[0] = ASTnode('')
    p[0].children_tuple_operations = [p[1]]
    p[0].children_tuple_atoms = [p[2]]


def p_zero_or_more_tup_op_tup_atom2(p):
    '''zero_or_more_tup_op_tup_atom : tuple_operation tuple_atom zero_or_more_tup_op_tup_atom'''
    p[0] = p[3]
    p[0].children_tuple_operations.insert(0, p[1])
    p[0].children_tuple_atoms.insert(0, p[2])


def p_zero_or_more_tup_op_tup_atom3(p):
    '''zero_or_more_tup_op_tup_atom : '''


def p_tuple_expression(p):
    '''tuple_expression : tuple_atom zero_or_more_tup_op_tup_atom'''
    # print('tuplevariable_definition(', p[0], ')')
    # p[0] = ASTnode('tuple_expression')
    p[0] = p[1]


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    p[0] = ASTnode('tuple_operation')
    p[0].value = p[1]


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT'''
    p[0] = ASTnode('tuple_atom')
    p[0].value = p[1]
    # p[0] = p[1]


def p_tuple_atom2(p):
    '''tuple_atom : function_call'''
    p[0] = p[1]


def p_tuple_atom3(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE'''
    p[0] = p[2]


def p_tuple_atom4(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEDOT  constant_expression RSQUARE'''
    p[0] = p[2]


def p_tuple_atom5(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''
    p[0] = p[2]


def p_function_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    # print('function_call( ', p[1], ')')
    p[0] = ASTnode('function_call')
    p[0].value = p[1]


def p_function_call2(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    # print('function_call( ', p[1], ')')
    p[0] = ASTnode('function_call')
    p[0].value = p[1]


def p_zero_or_more_comma_simple_expression(p):
    '''zero_or_more_comma_simple_expression : COMMA simple_expression'''
    p[0] = ASTnode('')
    p[0].children_simple_expressions = [p[2]]


def p_zero_or_more_comma_simple_expression2(p):
    '''zero_or_more_comma_simple_expression : COMMA simple_expression zero_or_more_comma_simple_expression'''
    p[0] = p[3]
    p[0].children_simple_expressions.insert(0, p[2])


def p_zero_or_more_comma_simple_expression3(p):
    '''zero_or_more_comma_simple_expression : '''


def p_arguments(p):
    '''arguments : simple_expression zero_or_more_comma_simple_expression'''
    p[0] = ASTnode('arguments')
    p[0].child_simple_expressions = p[2]


def p_atom(p):
    '''atom : function_call'''
    p[0] = ASTnode('function_call')
    p[0].value = p[1]


def p_atom2(p):
    '''atom : NUMBER_LITERAL'''
    p[0] = ASTnode('NUMBER_LITERAL')
    p[0].value = p[1]


def p_atom3(p):
    '''atom : STRING_LITERAL'''
    p[0] = ASTnode('STRING_LITERAL')
    p[0].value = p[1]


def p_atom4(p):
    '''atom : varIDENT'''
    p[0] = ASTnode('varIDENT')
    p[0].value = p[1]


def p_atom5(p):
    '''atom : constIDENT'''
    p[0] = ASTnode('constIDENT')
    p[0].value = p[1]


def p_atom6(p):
    '''atom : LPAREN simple_expression RPAREN'''
    # print('atom')
    p[0] = ASTnode('simple_expression')
    p[0].child_simple_expression = p[2]


def p_atom7(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    # print('atom')
    p[0] = ASTnode('select_constant')
    p[0].child_constant_expression = p[3]


def p_factor(p):
    '''factor : atom'''
    # p[0] = ASTnode('factor')
    # p[0].child_atom = p[1]
    p[0] = p[1]  # factor is an atom


def p_factor2(p):
    '''factor : MINUS atom'''
    # p[0] = ASTnode('factor')
    # p[0].child_atom = p[2]
    p[0] = p[2]


def p_zero_or_more_mult_factor(p):
    '''zero_or_more_mult_factor : MULT factor'''
    p[0] = ASTnode('')
    p[0].children_factors = [p[2]]


def p_zero_or_more_mult_factor2(p):
    '''zero_or_more_mult_factor : MULT factor zero_or_more_mult_factor'''
    p[0].children_factors.insert(0, p[2])


def p_zero_or_more_mult_factor3(p):
    '''zero_or_more_mult_factor : '''


def p_zero_or_more_div_factor(p):
    '''zero_or_more_div_factor : DIV factor'''
    p[0] = ASTnode('')
    p[0].children_factors = [p[2]]


def p_zero_or_more_div_factor2(p):
    '''zero_or_more_div_factor : DIV factor zero_or_more_div_factor'''
    p[0] = p[3]
    p[0].children_factors.insert(0, p[2])


def p_zero_or_more_div_factor3(p):
    '''zero_or_more_div_factor : '''


def p_term(p):
    '''term : factor'''
    # p[0] = ASTnode('term')
    # p[0].value = p[1]
    p[0] = p[1]


def p_term2(p):
    '''term : factor zero_or_more_div_factor'''
    # p[0] = ASTnode('term')
    # p[0].value = p[1]
    # p[0].child_div_factors = p[2]
    p[0] = p[1]


def p_term3(p):
    '''term : factor zero_or_more_mult_factor'''
    # p[0] = ASTnode('term')
    # p[0].child_first_factor = p[1]
    # p[0].child_mult_factors = p[2]
    p[0] = p[1]


def p_zero_or_more_minus_term(p):
    '''zero_or_more_minus_term : MINUS term'''
    p[0] = ASTnode('')
    p[0].children_terms = [p[2]]


def p_zero_or_more_minus_term2(p):
    '''zero_or_more_minus_term : MINUS term zero_or_more_minus_term'''
    p[0] = p[3]
    p[0].children_terms.insert(0, p[2])


def p_zero_or_more_minus_term3(p):
    '''zero_or_more_minus_term : '''


def p_zero_or_more_plus_term(p):
    '''zero_or_more_plus_term : PLUS term'''
    p[0] = ASTnode('')
    p[0].children_terms = [p[2]]


def p_zero_or_more_plus_term2(p):
    '''zero_or_more_plus_term : PLUS term zero_or_more_plus_term'''
    p[0] = p[3]
    p[0].children_terms.insert(0, p[2])


def p_zero_or_more_plus_term3(p):
    '''zero_or_more_plus_term : '''


def p_simple_expression(p):
    '''simple_expression : term zero_or_more_plus_term'''
    # p[0] = ASTnode('simple_expression')
    # p[0].child_first_term = p[1]
    # p[0].child_plus_terms = p[2]
    p[0] = p[1]  # simple expression is a term


def p_simple_expression2(p):
    '''simple_expression : term zero_or_more_minus_term'''
    # p[0] = ASTnode('simple_expression')
    # p[0].child_first_term = p[1]
    # p[0].child_minus_terms = p[2]
    p[0] = p[1]


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print('syntax error @', p)
    raise SystemExit


parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print('Khoa Nguyen - 272580')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        result = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        tree_print.treeprint(result, outformat)

        # data = codecs.open(ns.file, encoding='utf-8').read()
        # result = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        # if result is None:
        #     print('syntax OK')
