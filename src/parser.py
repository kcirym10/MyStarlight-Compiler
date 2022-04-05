from sly import Parser
from lexer import StartlightLexer
import os.path


class StartlightParser(Parser):

    # Import the set of tokens made by the Lexer
    # Required by the parser
    tokens = StartlightLexer.tokens
    debugfile = 'parser.out'

    # Set of rules for sintaxis

    # Program
    @_('PROGRAM ID ";" opt_vars opt_classes opt_funcs main')
    def program(self, p):
        print("Successfully compiled uwu")
        pass

    @_('vars', 'eps')
    def opt_vars(self, p):
        pass

    @_('classes', 'eps')
    def opt_classes(self, p):
        pass

    @_('functions', 'eps')
    def opt_funcs(self, p):
        pass

    # Vars
    @_('VAR var_type')
    def vars(self, p):
        pass

    @_('simple ";" more_var_types', 'compound ";" more_var_types')
    def var_type(self, p):
        pass

    @_('var_type', 'eps')
    def more_var_types(self, p):
        pass

    @_("type ID moreids")
    def simple(self, p):
        pass

    @_('"," ID moreids', 'eps')
    def moreids(self, p):
        pass

    @_('CLASS_ID ID moreids', 'type ID "[" CTE_INT two_dim "]" more_arr_ids')
    def compound(self, p):
        pass

    @_('"," ID "[" CTE_INT two_dim "]" more_arr_ids', 'eps')
    def more_arr_ids(self, p):
        pass

    @_('"," CTE_INT', 'eps')
    def two_dim(self, p):
        pass

    # Classes
    @_('CLASS CLASS_ID opt_derivation "{" opt_vars opt_methods "}" classes', 'eps')
    def classes(self, p):
        pass

    @_('DERIVES CLASS_ID', 'eps')
    def opt_derivation(self, p):
        pass

    @_('methods', 'eps')
    def opt_methods(self, p):
        pass

    # Methods
    @_('METHODS ":" functions')
    def methods(self, p):
        pass

    # Functions
    @_('function', 'eps')
    def functions(self, p):
        pass

    @_('FUNC func_types ID "(" opt_param ")" opt_vars "{" body "}" functions')
    def function(self, p):
        pass

    @_('type', 'VOID')
    def func_types(self, p):
        pass

    @_('param moreparams', 'eps')
    def opt_param(self, p):
        pass

    @_('"," param opt_param', 'eps')
    def moreparams(self, p):
        pass

    # Param
    @_('type ID')
    def param(self, p):
        pass

    # Type
    @_('INT', 'FLOAT', 'CHAR')
    def type(self, p):
        pass

    # Body
    @_('opt_stmts opt_return')
    def body(self, p):
        pass

    @_('statements opt_stmts', 'eps')
    def opt_stmts(self, p):
        pass

    '''@_('opt_stmts', 'eps')
    def more_stmts(self, p):
        pass'''

    @_('RETURN "(" expression ")" ";" opt_return', 'eps')
    def opt_return(self, p):
        pass

    # Statements
    @_('print', 'read', 'assign', 'conditional', 'cycles', 'call_func')
    def statements(self, p):
        pass

    # Print
    @_('PRINT "(" p_args ")" ";"')
    def print(self, p):
        pass

    @_('CTE_STRING more_args', 'expression more_args')
    def p_args(self, p):
        pass

    @_('"," p_args', 'eps')
    def more_args(self, p):
        pass

    # Read
    @_('READ "(" variable ")" ";"')
    def read(self, p):
        pass

    # Assign
    @_('variable "=" expression ";"')
    def assign(self, p):
        pass

    # Conditional
    @_('IF "(" expression ")" "{" body "}" opt_else')
    def conditional(self, p):
        pass

    @_('ELSE "{" body "}"', 'eps')
    def opt_else(self, p):
        pass

    # Cycles
    @_('for_loop', 'while_loop')
    def cycles(self, p):
        pass

    @_('FOR "(" ID "=" expression TO expression ")" "{" body "}"')
    def for_loop(self, p):
        pass

    @_('WHILE "(" expression ")" "{" body "}"')
    def while_loop(self, p):
        pass

    # Call Func
    @_('call_func_body ";"')
    def call_func(self, p):
        pass

    @_('ID opt_class_func "(" opt_call_params ")" ')
    def call_func_body(self, p):
        pass

    @_(' "." ID', 'eps')
    def opt_class_func(self, p):
        pass

    @_('expression more_expressions', 'eps')
    def opt_call_params(self, p):
        pass

    @_('"," opt_call_params', 'eps')
    def more_expressions(self, p):
        pass

    # Variable
    @_('ID opt_class_func opt_arr_call')
    def variable(self, p):
        pass

    @_(' "[" expression opt_dim_call "]"', 'eps')
    def opt_arr_call(self, p):
        pass

    @_(' "," expression', 'eps')
    def opt_dim_call(self, p):
        pass

    # Expression (OR)
    @_('t_exp exp_or')
    def expression(self, p):
        pass

    @_('"|" expression', 'eps')
    def exp_or(self, p):
        pass

    # T_EXP (AND)
    @_('g_exp t_and')
    def t_exp(self, p):
        pass

    @_('"&" t_exp', 'eps')
    def t_and(self, p):
        pass

    # G_EXP
    @_('m_exp g_exp_opers')
    def g_exp(self, p):
        pass

    @_('"<" m_exp', '">" m_exp', 'GREATER_OR_EQUAL_TO m_exp', 'LESS_OR_EQUAL_TO m_exp', 'NOT_EQUAL_TO m_exp', 'EQUAL_TO m_exp', 'eps')
    def g_exp_opers(self, p):
        pass

    # M_EXP (sum and rest)
    @_('t m_opers')
    def m_exp(self, p):
        pass

    @_('"+" m_exp', '"-" m_exp', 'eps')
    def m_opers(self, p):
        pass

    # T (multuplication and division)
    @_('f t_opers')
    def t(self, p):
        pass

    @_('"*" t', '"/" t', 'eps')
    def t_opers(self, p):
        pass

    # F
    @_('"(" expression ")"', 'variable', 'call_func_body', 'var_cte')
    def f(self, p):
        pass

    # Var_cte integer, float, char, string
    @_('CTE_INT', 'CTE_FLOAT', 'CTE_CHAR', 'CTE_STRING')
    def var_cte(self, p):
        pass

    # Main
    @_('MAIN "(" ")" opt_vars "{" body "}"')
    def main(self, p):
        pass

    # Epsilon, describes an empty production

    @_('')
    def eps(self, p):
        pass


if __name__ == '__main__':
    lexer = StartlightLexer()
    parser = StartlightParser()
    print("==PARSER SLY==\n")

    try:

        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'test.txt')
        f = open(filename)
        # print(f.read())

        # f = open("test.txt", "r")  # inserta nombre de archivo
        s = ""
        for s1 in f:
            s += s1

        result = parser.parse(lexer.tokenize(s))
        print(result)
    except EOFError:
        print("Error" + EOFError)
