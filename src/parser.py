from sly import Parser
from lexer import StartlightLexer
from quadruples import Quadruples
from record import Record
from symTable import symTable
from symTableManager import symTableManager
import os.path
import copy


class StartlightParser(Parser):

    # Import the set of tokens made by the Lexer
    # Required by the parser
    tokens = StartlightLexer.tokens
    debugfile = 'parser.out'

    # Set of rules for sintaxis

    # Program
    @_('PROGRAM np_create_global_symTable ID np_program_record ";" opt_vars opt_classes opt_funcs main')
    def program(self, p):
        print("Successfully compiled uwu")
    
    # Initializes all global variables
    @_('')
    def np_create_global_symTable(self, p):
        #print("Program type")
        global symMngr
        symMngr = symTableManager()
        global record 
        record = Record()
        global quads
        quads = Quadruples()
        record.setType(record.getProgramType())
    
    @_('')
    def np_program_record(self, p):
        symMngr.insertRecord(p[-1], record.returnRecord())
        record.clearCurrentRecord()
        

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
    @_('VAR np_create_var_table var_type')
    def vars(self, p):
        pass

    @_('')
    def np_create_var_table(self, p):
        # 1 Check if current table already has a vars table
        if not symMngr[-1].hasVarTable():
            record.setType("Var Table")
            # TODO: Need parent ref
            record.setChildRef(symMngr.getNewSymTable())
            symMngr.insertRecord('VARS',record.returnRecord())
            record.clearCurrentRecord()
            print(symMngr[-1])
        else:
            # What to do when table already exists?
            # Created at function parameters
            print(":)")
    
    @_('')
    def np_exit_scope(self, p):
        symMngr.popRecord()
        #print(symMngr)

    @_('simple ";" more_var_types', 'compound ";" more_var_types')
    def var_type(self, p):
        pass

    @_('var_type', 'eps')
    def more_var_types(self, p):
        pass

    @_("type ID np_save_id moreids")
    def simple(self, p):
        pass

    # Sets current type to each record and inserts it in current vars table
    @_('')
    def np_save_id(self, p):
        if symMngr.canPushOrPop:
            if symMngr.isVarKeyDeclared(p[-1]):
                record.setType(symMngr.getCurrentType())
                symMngr.insertVarRecord(p[-1], record.returnRecord())
                record.clearCurrentRecord()
            else:
                print(f"Multiple declaration of key: \"{p[-1]}\"")

    @_('"," ID np_save_id moreids', 'eps')
    def moreids(self, p):
        pass

    @_('CLASS_ID np_class_id ID np_save_id moreids', 'type ID "[" CTE_INT two_dim "]" more_arr_ids')
    def compound(self, p):
        pass

    @_('')
    def np_class_id(self, p):
        # TODO Check if class_id defined in semantic cube
        symMngr.setCurrentType(p[-1])

    @_('"," ID np_save_id "[" CTE_INT two_dim "]" more_arr_ids', 'eps')
    def more_arr_ids(self, p):
        pass

    @_('"," CTE_INT', 'eps')
    def two_dim(self, p):
        pass

    # Classes
    @_('CLASS np_prepare_class CLASS_ID np_save_func_id opt_derivation "{" opt_vars opt_methods "}" np_exit_scope classes', 'eps')
    def classes(self, p):
        pass

    @_('')
    def np_prepare_class(self, p):
        symMngr.setCurrentType(record.getClassType())

    @_('DERIVES CLASS_ID np_copy_class_record', 'eps')
    def opt_derivation(self, p):
        pass

    @_('')
    def np_copy_class_record(self, p):
        print(p[-4])
        if len(symMngr) > 1:
            classRecord = symMngr[-2].getFuncRecord(p[-1])
            if classRecord:
                print(classRecord['childRef'])
                
                # Need to create copy of contents into a new symTable object
                # deepcopy from the copy module creates a new object and copies all of the children from the
                # original object. These will not be modified in any changes.
                symMngr[-2][p[-4]] = copy.deepcopy(classRecord) # Gets pointer to record
                symMngr.pop()
                symMngr.pushTable(symMngr[-1][p[-4]]['childRef'])
            else:
                print("Undefined class derivation")
            

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

    @_('FUNC func_types ID np_save_func_id "(" np_create_var_table opt_param ")" opt_vars "{" body "}" np_exit_scope functions')
    def function(self, p):
        pass

    @_('')
    def np_save_func_id(self, p):
        if symMngr.isKeyDeclared(p[-1]):
            record.setType(symMngr.getCurrentType())
            record.setChildRef(symMngr.getNewSymTable())
            symMngr.insertRecord(p[-1], record.returnRecord())
            symMngr.pushTable(record.getChildRef())
            record.clearCurrentRecord()
        else:
            symMngr.canPushOrPop = False
            print(f"Multiple declaration of key: \"{p[-1]}\"")

    # Set current type in symMngr to void
    @_('type', 'VOID')
    def func_types(self, p):
        if (p[-1] == "void"):
            symMngr.setCurrentType(p[-1])

    @_('param moreparams', 'eps')
    def opt_param(self, p):
        pass

    @_('"," param opt_param', 'eps')
    def moreparams(self, p):
        pass

    # Param
    @_('type ID np_save_id')
    def param(self, p):
        pass

    # Type
    @_('INT', 'FLOAT', 'CHAR')
    def type(self, p):
        symMngr.setCurrentType(p[-1]) # sets the symMngr's current type

    # Body
    @_('opt_stmts')
    def body(self, p):
        pass

    @_('statements opt_stmts', 'eps')
    def opt_stmts(self, p):
        pass

    # Statements
    @_('print', 'read', 'assign', 'conditional', 'cycles', 'call_func', 'function_return')
    def statements(self, p):
        pass

    # Print Statement
    @_('PRINT "(" p_args ")" ";"')
    def print(self, p):
        pass

    @_('CTE_STRING more_args', 'expression more_args')
    def p_args(self, p):
        pass

    @_('"," p_args', 'eps')
    def more_args(self, p):
        pass

    # Read Statement
    @_('READ "(" variable ")" ";"')
    def read(self, p):
        pass

    # Assign Statement
    @_('variable "=" expression ";"')
    def assign(self, p):
        pass

    # Conditional Statement
    @_('IF "(" expression ")" "{" body "}" opt_else')
    def conditional(self, p):
        pass

    @_('ELSE "{" body "}"', 'eps')
    def opt_else(self, p):
        pass

    # Cycles Statement
    @_('for_loop', 'while_loop')
    def cycles(self, p):
        pass

    @_('FOR "(" ID "=" expression TO expression ")" "{" body "}"')
    def for_loop(self, p):
        pass

    @_('WHILE "(" expression ")" "{" body "}"')
    def while_loop(self, p):
        pass

    # Call Func Statement
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

    # Return Statement
    @_('RETURN "(" expression ")" ";"')
    def function_return(self, p):
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

    @_('"|" np_push_or_operator expression', 'eps')
    def exp_or(self, p):
        pass
    
    # Passes tuple of or operators to compare
    @_('')
    def np_push_or_operator(self, p):
        quads.createIfTopIs(("|"))

    # T_EXP (AND)
    @_('g_exp t_and')
    def t_exp(self, p):
        pass

    @_('"&" np_push_and_operator t_exp', 'eps')
    def t_and(self, p):
        pass

    # Passes tuple of and operators to compare
    @_('')
    def np_push_and_operator(self, p):
        quads.createIfTopIs(("&"))

    # G_EXP
    @_('m_exp g_exp_opers')
    def g_exp(self, p):
        pass

    @_('"<" np_push_g_operator m_exp', '">" np_push_g_operator m_exp', 'GREATER_OR_EQUAL_TO np_push_g_operator m_exp', 
        'LESS_OR_EQUAL_TO np_push_g_operator m_exp', 'NOT_EQUAL_TO np_push_g_operator m_exp', 'EQUAL_TO np_push_g_operator m_exp', 'eps')
    def g_exp_opers(self, p):
        pass

    # Passes tuple of g operators to compare
    @_('')
    def np_push_g_operator(self, p):
        quads.createIfTopIs(("<", ">", ">=", "<=", "!=", "=="))

    # M_EXP (sum and rest)
    @_('t m_opers')
    def m_exp(self, p):
        pass

    @_('"+" np_push_m_operator m_exp', '"-" np_push_m_operator m_exp', 'eps')
    def m_opers(self, p):
        pass
    
    # Passes tuple of m operators to compare
    @_('')
    def np_push_m_operator(self, p):
        quads.createIfTopIs(("+", "-"))

    # T (multuplication and division)
    @_('f t_opers')
    def t(self, p):
        pass

    @_('"*" np_t_push_operator t', '"/" np_t_push_operator t', 'eps')
    def t_opers(self, p):
        pass
    
    # Passes tuple of t operators to compare
    @_('')
    def np_t_push_operator(self, p):
        quads.createIfTopIs(('*', '/'))
    # F
    @_('"(" expression ")"', 'variable', 'call_func_body', 'var_cte')
    def f(self, p):
        pass

    # Var_cte integer, float, char, string
    @_('CTE_INT', 'CTE_FLOAT', 'CTE_CHAR')
    def var_cte(self, p):
        if symMngr.canPushOrPop:
            # If no global variable table
            if not symMngr[0].hasVarTable():
                record.setType("Var Table")
                # TODO: Need parent ref
                record.setChildRef(symMngr.getNewSymTable())
                symMngr[0].saveRecord('VARS',record.returnRecord())
                record.clearCurrentRecord()
                print(symMngr[-1])
            
            print(type(p[-1]))
            symMngr[0]['VARS']['childRef'][p[-1]] = p[-1]

    # Main
    @_('MAIN np_save_main_id "(" ")" opt_vars "{" body "}"')
    def main(self, p):
        pass

    @_('')
    def np_save_main_id(self, p):
        record.setType(record.getMainType())
        #print(record.currentRecord["type"], "\n\n")
        record.setChildRef(symMngr.getNewSymTable())
        symMngr.insertRecord(p[-1], record.returnRecord())
        symMngr.pushTable(record.getChildRef())
        record.clearCurrentRecord()

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
        #print(result)
        print(symMngr)
        print(quads.pOperators) # TODO: Fix Var Table and Sym Table
    except EOFError:
        print("Error" + EOFError)
