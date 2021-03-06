from distutils.log import error
import os.path
import copy

from sly import Parser
from lexer import StartlightLexer
from quadruples import Quadruples
from record import Record
from symTable import symTable
from symTableManager import symTableManager
from virtualMemory import VirtualMemory
from helper import errorList

class StartlightParser(Parser):

    # Import the set of tokens made by the Lexer
    # Required by the parser
    tokens = StartlightLexer.tokens
    debugfile = 'parser.out'

    # Set of rules for sintaxis

    # Program
    @_('PROGRAM np_create_global_symTable ID np_program_record ";" opt_vars opt_classes opt_funcs main end')
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
        global vMem
        vMem = VirtualMemory()
        record.setType(record.getProgramType())
        # Create first quad GOTO Main
        quads.createGotoMain()

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
        if symMngr.canPushOrPop:
            # 1 Check if current table already has a vars table
            if not symMngr[-1].hasVarTable():
                record.setType("Var Table")
                # TODO: Need parent ref
                record.setChildRef(symMngr.getNewSymTable())
                symMngr.insertRecord('VARS', record.returnRecord())
                record.clearCurrentRecord()
            # else:
            #     # What to do when table already exists?
            #     # Created at function parameters
            #     print(":)")

    @_('')
    def np_exit_scope(self, p):
        vMem.resetLocal()
        quads.resetAvail()
        symMngr.popRecord()

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
                if str.islower(symMngr.getCurrentType()):
                    if len(symMngr) == 1:
                        memAddress = vMem.nextGlobal(symMngr.getCurrentType())
                    else:
                        memAddress = vMem.nextLocal(symMngr.getCurrentType())
                    record.setMemoryAdress(memAddress)
                symMngr.insertVarRecord(p[-1], record.returnRecord())
                record.clearCurrentRecord()
            else:
                print(f"Multiple declaration of key: \"{p[-1]}\"")
                errorList.append(f"Multiple declaration of key: \"{p[-1]}\"")

    @_('"," ID np_save_id moreids', 'eps')
    def moreids(self, p):
        pass

    @_('CLASS_ID np_class_id ID np_save_id moreids', 'type ID "[" CTE_INT two_dim "]" more_arr_ids')
    def compound(self, p):
        pass

    @_('')
    def np_class_id(self, p):
        if symMngr.canPushOrPop:
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
        if symMngr.canPushOrPop:
            if len(symMngr) > 1:
                classRecord = symMngr[-2].getFuncRecord(p[-1])
                if classRecord:

                    # Need to create copy of contents into a new symTable object
                    # deepcopy from the copy module creates a new object and copies all of the children from the
                    # original object. These will not be modified in any changes.
                    # Gets pointer to record
                    symMngr[-2][p[-4]] = copy.deepcopy(classRecord)
                    symMngr.pop()
                    symMngr.pushTable(symMngr[-1][p[-4]]['childRef'])
                else:
                    print("Undefined class derivation")
                    errorList.append("Undefined class derivation")

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

    @_('FUNC func_types ID np_save_func_id "(" np_create_var_table opt_param ")" opt_vars "{" body "}" np_endfunc np_exit_scope functions')
    def function(self, p):
        pass

    @_('')
    def np_save_func_id(self, p):
        if symMngr.canPushOrPop:
            # Check for unique global variable naming and function naming
            # if 'VARS' in symMngr[0]:
            #     if p[-1] in symMngr[0]['VARS']['childRef']:
            #         kErr = 0
            #     else:
            #         kErr = None
            # if not symMngr.isKeyDeclared(p[-1]) and kErr is None:
            if not symMngr.isKeyDeclared(p[-1]):
                record.setType(symMngr.getCurrentType())
                record.setQuadNumber(quads.ip)
                record.setSizeStruct()
                record.setChildRef(symMngr.getNewSymTable(p[-1]))
                symMngr.insertRecord(p[-1], record.returnRecord())
                symMngr.pushTable(record.getChildRef())
                record.clearCurrentRecord()
            else:
                symMngr.canPushOrPop = False
                print(f"Multiple declaration of key: \"{p[-1]}\"")
                errorList.append(f"Multiple declaration of key: \"{p[-1]}\"")
        return

    @_('')
    def np_endfunc(self, p):
        if symMngr.canPushOrPop:
            #print(symMngr[-1].parentRef[symMngr[-1].parentName]['size'])
            # Save the size of the current function scope to its size parameter
            symMngr.setFunctionSize(vMem.getLocalSize(), quads.avail.getTempSize())
            # Create ENDFUNC Quadruple
            quads.createEndFunc()
            # Delete vars table from current scope
            symMngr[-1].pop('VARS')

    # Set current type in symMngr to void
    @_('type', 'VOID')
    def func_types(self, p):
        if (p[-1] == "void"):
            symMngr.setCurrentType(p[-1])

    @_('param', 'eps')
    def opt_param(self, p):
        pass

    @_('"," param opt_param', 'eps')
    def moreparams(self, p):
        pass

    # Param
    @_('type ID np_save_id np_save_param moreparams')
    def param(self, p):
        pass

    # Saves the current type of the param to the signature list
    @_('')
    def np_save_param(self, p):
        symMngr[-1].addToSignature(symMngr.currentType)

    # Type
    @_('INT', 'FLOAT', 'CHAR')
    def type(self, p):
        if symMngr.canPushOrPop:
            symMngr.setCurrentType(p[-1])  # sets the symMngr's current type

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

    @_('CTE_STRING np_create_print_quad more_args', 'expression np_create_print_quad more_args')
    def p_args(self, p):
        pass

    @_('')
    def np_create_print_quad(self, p):
        if symMngr.canPushOrPop:
            quads.createPRQuad(p[-1], True)

    @_('"," p_args', 'eps')
    def more_args(self, p):
        pass

    # Read Statement
    @_('READ "(" r_args ")" ";"')
    def read(self, p):
        pass

    @_('variable np_create_read_quad more_r_args')
    def r_args(self, p):
        pass

    @_('"," r_args', 'eps')
    def more_r_args(self, p):
        pass

    @_('')
    def np_create_read_quad(self, p):
        if symMngr.canPushOrPop:
            quads.createPRQuad(p[-1], False)

    # Assign Statement
    @_('variable "=" np_push_operator expression ";" np_check_assignment_operator')
    def assign(self, p):
        pass

    @_('')
    def np_check_assignment_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("="))

    # Conditional Statement
    @_('IF "(" expression ")" np_if "{" body "}" opt_else np_end_if')
    def conditional(self, p):
        pass

    @_('')
    def np_if(self, p): # Implement if NP 1
        quads.createGotoF()

    @_('')
    def np_end_if(self, p):
        quads.fillGotos()

    @_('ELSE np_else "{" body "}"', 'eps')
    def opt_else(self, p):
        pass
    
    @_('')
    def np_else(self, p):
        quads.createGoto()

    # Cycles Statement
    @_('for_loop', 'while_loop')
    def cycles(self, p):
        pass

    @_('FOR "(" ID "=" expression TO expression ")" "{" body "}"')
    def for_loop(self, p):
        pass

    @_('WHILE np_cycle_start "(" expression ")" np_while "{" body "}" np_while_return')
    def while_loop(self, p):
        pass

    @_('')
    def np_cycle_start(self, p):
        if symMngr.canPushOrPop:
            quads.addJump()

    @_('')
    def np_while(self, p):
        if symMngr.canPushOrPop:
            quads.createGotoF()

    @_('')
    def np_while_return(self, p):
        if symMngr.canPushOrPop:
            quads.createWhileGoto()

    # Call Func Statement
    @_('call_func_body ";"')
    def call_func(self, p):
        pass

    @_('ID opt_class_func np_func_call "(" np_func_ERA opt_call_params ")" np_func_gosub')
    def call_func_body(self, p):
        pass

    @_(' "." ID', 'eps')
    def opt_class_func(self, p):
        if p[0] == ".":
            #print(p[-1])
            return p[-1]

    # If the function id does not exist we generate an error
    @_('')
    def np_func_call(self, p):
        if symMngr.canPushOrPop:
            if p[-1] is None:
                if not symMngr.isFuncDeclared(p[-2]):
                    errorList.append(f"Undefined function call id: {p[-2]}")
                    print(f"Undefined function call id: {p[-2]}")
            #     print("FUNCTION CALL ", p[-2])
            # else:
            #     print("CLASS FUNCTION CALL")

    @_('')
    def np_func_ERA(self, p):
        if symMngr.canPushOrPop:
            if p[-3] is None:
                if symMngr.isFuncDeclared(p[-4]):
                    funcSize = symMngr[0][p[-4]]['size']
                    paramSignature = symMngr[0][p[-4]]['childRef']['paramSignature']
                    quads.createERA(funcSize, paramSignature)

    @_('')
    def np_func_gosub(self, p):
        pass
        if symMngr.canPushOrPop:
            if p[-6] is None:
                if symMngr.isFuncDeclared(p[-7]):
                    quadNum = symMngr.searchAtomic(p[-7])['quadNum']
                    quads.createGoSub(quadNum)
            # else, search the function in classes
                    

    @_('expression np_func_param more_expressions', 'eps')
    def opt_call_params(self, p):
        pass

    @_('')
    def np_func_param(self, p):
        quads.createParam()

    @_('"," opt_call_params', 'eps')
    def more_expressions(self, p):
        pass

    # Return Statement
    @_('RETURN "(" expression ")" ";"')
    def function_return(self, p):
        pass

    # Variable
    @_('ID  opt_class_func opt_arr_call np_push_var_operand')
    def variable(self, p):
        pass

    # If any of the two previous rules returns something then
    # the a normal variable is not added
    @_('')
    def np_push_var_operand(self, p):
        if symMngr.canPushOrPop:
            if p[-2] == None and p[-1] == None:
                # If the variable is declared then we can add it
                operand = p[-3]
                record = symMngr.searchAtomic(operand)
                if record:
                    #print(operand, ' ', record['address'])
                    #quads.pushOperandType(operand, record['type'])
                    quads.pushOperandType(record["address"], record['type'])
                else:
                    print(f"Key: \"{p[-3]}\" is not defined")
                    errorList.append(f"Key: \"{p[-3]}\" is not defined")

    @_(' "[" expression opt_dim_call "]"', 'eps')
    def opt_arr_call(self, p):
        pass

    @_(' "," expression', 'eps')
    def opt_dim_call(self, p):
        pass

    # Expression (OR)
    @_('t_exp np_check_or_operator exp_or')
    def expression(self, p):
        pass

    @_('')
    def np_check_or_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("|"))

    @_('"|" np_push_operator expression', 'eps')
    def exp_or(self, p):
        pass

    @_('')
    def np_push_operator(self, p):
        if symMngr.canPushOrPop:
            quads.pushOperator(p[-1])

    # Passes tuple of or operators to compare
    @_('')
    def np_push_or_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("|"))

    # T_EXP (AND)
    @_('g_exp np_check_and_operator t_and')
    def t_exp(self, p):
        pass

    @_('')
    def np_check_and_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("&"))

    @_('"&" np_push_operator t_exp', 'eps')
    def t_and(self, p):
        pass

    # G_EXP
    @_('m_exp np_check_g_operator g_exp_opers')
    def g_exp(self, p):
        pass

    # Passes tuple of g operators to compare
    @_('')
    def np_check_g_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("<", ">", ">=", "<=", "!=", "=="))

    @_('"<" np_push_operator g_exp', '">" np_push_operator g_exp', 'GREATER_OR_EQUAL_TO np_push_operator g_exp',
        'LESS_OR_EQUAL_TO np_push_operator g_exp', 'NOT_EQUAL_TO np_push_operator g_exp', 'EQUAL_TO np_push_operator g_exp', 'eps')
    def g_exp_opers(self, p):
        pass

    # M_EXP (sum and rest)
    @_('t np_check_m_operator m_opers')
    def m_exp(self, p):
        pass

    # Passes tuple of m operators to compare
    @_('')
    def np_check_m_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(("+", "-"))

    @_('"+" np_push_operator m_exp', '"-" np_push_operator m_exp', 'eps')
    def m_opers(self, p):
        pass

    # T (multuplication and division)
    @_('f np_check_t_operator t_opers')
    def t(self, p):
        pass

    # Passes tuple of t operators to compare
    @_('')
    def np_check_t_operator(self, p):
        if symMngr.canPushOrPop:
            quads.createIfTopIs(('*', '/'))
        pass

    @_('"*" np_push_operator t', '"/" np_push_operator t', 'eps')
    def t_opers(self, p):
        pass

    # F
    @_('"(" np_add_fake_bottom expression ")" np_rem_fake_bottom', 'variable', 'call_func_body', 'var_cte')
    def f(self, p):
        pass

    @_('')
    def np_add_fake_bottom(self, p):
        if symMngr.canPushOrPop:
            quads.pushOperator('(')

    @_('')
    def np_rem_fake_bottom(self, p):
        if symMngr.canPushOrPop and len(errorList) == 0:
            if quads.operatorStack[-1] == '(':
                quads.operatorStack.pop()

    # Var_cte integer, float, char, string
    @_('CTE_INT', 'CTE_FLOAT', 'CTE_CHAR')
    def var_cte(self, p):
        if symMngr.canPushOrPop:
            # If no global variable table
            if not symMngr[0].hasVarTable():
                record.setType("Var Table")
                record.setChildRef(symMngr.getNewSymTable())
                symMngr[0].saveRecord('VARS', record.returnRecord())
                record.clearCurrentRecord()
            # Save into constants table
            if 'CTE' not in symMngr[0]:
                record.setType('cte')
                record.setChildRef(symMngr.getNewSymTable())
                symMngr[0].saveRecord('CTE', record.returnRecord())
                record.clearCurrentRecord()

            searchRes = symMngr.searchAtomic(str(p[-1]))
            # Gets the data type from the constant token
            cteType = str(type(p[-1]).__name__)
            if searchRes == None:
                memAddress = vMem.nextConstant(cteType)
                symMngr[0]['VARS']['childRef'][str(p[-1])] = memAddress
                symMngr[0]['CTE']['childRef'][str(p[-1])] = memAddress
            else:
                memAddress = searchRes
                #print("Value: ", p[-1], " Address: ", searchRes)

            # Insert into quadruples
            quads.pushOperandType(memAddress, cteType)

    # Main

    @_('MAIN np_save_main_id "(" ")" opt_vars "{" body "}" np_exit_scope')
    def main(self, p):
        pass

    @_('')
    def np_save_main_id(self, p):
        if symMngr.canPushOrPop:
            record.setType(record.getMainType())
            #print(record.currentRecord["type"], "\n\n")
            record.setChildRef(symMngr.getNewSymTable())
            symMngr.insertRecord(p[-1], record.returnRecord())
            symMngr.pushTable(record.getChildRef())
            record.clearCurrentRecord()

            # Fill quad goto main
            quads.fillGotos()

    @_('')
    def end(self, p):
        if symMngr.canPushOrPop:
            quads.createEndProgram()
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
        # print(result)
        print(symMngr)
        print(quads.operatorStack)  # TODO: Fix Var Table and Sym Table
        print(quads.operandStack)
        print(quads.typeStack)
        print(quads.jumpStack)
        print(quads)
    except EOFError:
        print("Error" + EOFError)
