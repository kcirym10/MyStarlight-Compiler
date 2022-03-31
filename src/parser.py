from sly import Parser
from lexer import StartlightLexer


class StartlightParser(Parser):

    # Import the set of tokens made by the Lexer
    # Required by the parser
    tokens = StartlightLexer.tokens

    # Set of rules for sintaxis

    # Program
    @_('PROGRAM ID ";" opt_vars opt_classes opt_funcs')
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
    @_('VAR start_var')
    def vars(self, p):
        pass

    @_('v_types ids')
    def start_var(self, p):
        pass

    @_('type', 'CLASS_ID')
    def v_types(self, p):
        pass

    @_('ID opt_arr_def moreids ";" moretypes')
    def ids(self, p):
        pass

    @_('"[" CTE_INT opt_dim_def "]"', 'eps')
    def opt_arr_def(self, p):
        pass

    @_('"," CTE_INT', 'eps')
    def opt_dim_def(self, p):
        pass

    @_('"," ids', 'eps')
    def moreids(self, p):
        pass

    @_('start_var', 'eps')
    def moretypes(self, p):
        pass

    # Classes
    @_('CLASS CLASS_ID opt_derivation "{" opt_vars opt_methods "}"')
    def classes(self, p):
        pass

    @_('DERIVES CLASS_ID', 'eps')
    def opt_derivation(self, p):
        pass

    @_('vars', 'eps')
    def opt_vars(self, p):
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

    @_('statements more_stmts', 'eps')
    def opt_stmts(self, p):
        pass

    @_('opt_stmts', 'eps')
    def more_stmts(self, p):
        pass

    @_('RETURN "(" expression ")" ";"', 'eps')
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
    # Epsilon, describes an empty production

    @_('')
    def eps(self, p):
        pass
